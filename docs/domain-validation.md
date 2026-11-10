# ドメインの不変条件を確かめるパターン（`_validate`）

[README](../readme.md) / [バックエンド](backend.md) / [アーキテクチャ](architecture.md)

エンティティを作るたびに、そのエンティティ自身が不変条件（どの時点でも守られていないといけない決まり）を確かめる設計パターンの記録。
**MyUs では今は使っていない。** 使う場面が出てきたときの判断材料として残す。

例には MyUs の検索タグ（`SearchTagData`・`usecase/search_tag/core.py`）を使う。

## パターンの形

エンティティは次のものを持つ。

| 持つもの | 役割 |
|---|---|
| フィールド | `@dataclass(frozen=True, slots=True)` で持つ。frozen なので外から書き換えられない |
| `_validate()` | 不変条件を確かめ、`Result[None, ValidateError]` を返す |
| `_new()` | すべてのフィールドを受け取って作り、`_validate()` を通す。作る入り口はここに集める |
| `new()` | 新しく作るときの入り口。初期値（`id=0` など）を決めて `_new()` を呼ぶ |
| `update()` | 変えるときの入り口。変え方の決まりを確かめてから新しいオブジェクトを作り、`_validate()` を通す |

子のエンティティも同じ形にし、自分の不変条件は自分の `_validate()` で確かめる。親の `_validate()` は、子をまとめたときの決まり（数・重複）だけを確かめる。

検索タグをこのパターンで書くと次のようになる。

```python
from dataclasses import dataclass, replace
from api.utils.common.result import Result, ValidateError, ValidationError


_MAX_TAG_COUNT = 20
_MAX_NAME_LENGTH = 30


@dataclass(frozen=True, slots=True)
class SearchTags:
    author_id: int
    tags: tuple[SearchTag, ...]

    def _validate(self) -> Result[None, ValidateError]:
        if len(self.tags) > _MAX_TAG_COUNT:
            return Result.err(ValidationError("error.searchTagLimit"))
        names = [t.name for t in self.tags]
        if len(names) != len(set(names)):
            return Result.err(ValidationError("error.searchTagDuplicate"))
        sequences = [t.sequence for t in self.tags]
        if len(sequences) != len(set(sequences)):
            return Result.err(ValidationError("error.searchTagDuplicate"))
        return Result.ok(None)

    @classmethod
    def _new(cls, author_id: int, tags: tuple[SearchTag, ...]) -> Result[SearchTags, ValidateError]:
        obj = cls(author_id=author_id, tags=tags)
        if (ret := obj._validate()).is_err:
            return Result.err(ret.err_value)
        return Result.ok(obj)

    @classmethod
    def new(cls, author_id: int) -> Result[SearchTags, ValidateError]:
        return cls._new(author_id=author_id, tags=())

    def update(self, tags: tuple[SearchTag, ...]) -> Result[SearchTags, ValidateError]:
        id_map = {t.name: t.id for t in self.tags}
        new_tags = tuple(t.inherit_id(id_map.get(t.name, 0)) for t in tags)
        return SearchTags._new(author_id=self.author_id, tags=new_tags)

    def delete_ids(self, updated: SearchTags) -> list[int]:
        keep_ids = {t.id for t in updated.tags}
        return [t.id for t in self.tags if t.id not in keep_ids]


@dataclass(frozen=True, slots=True)
class SearchTag:
    id: int
    sequence: int
    name: str

    def _validate(self) -> Result[None, ValidateError]:
        if len(self.name) == 0 or len(self.name) > _MAX_NAME_LENGTH:
            return Result.err(ValidationError("error.searchTagNameLength"))
        return Result.ok(None)

    @classmethod
    def _new(cls, id: int, sequence: int, name: str) -> Result[SearchTag, ValidateError]:
        obj = cls(id=id, sequence=sequence, name=name)
        if (ret := obj._validate()).is_err:
            return Result.err(ret.err_value)
        return Result.ok(obj)

    @classmethod
    def new(cls, sequence: int, name: str) -> Result[SearchTag, ValidateError]:
        return cls._new(id=0, sequence=sequence, name=name)

    def inherit_id(self, id: int) -> SearchTag:
        return replace(self, id=id)
```

usecase は、決まりを確かめる処理を持たず、作って保存するだけになる。

```python
@Result.shield_exception()
def update_search_tags(author_id: int, tags: list[SearchTagIn]) -> Result[None, ValidateError]:
    current_ret = get_search_tags_data(author_id)  # 保存済みの検索タグから SearchTags を作る
    if current_ret.is_err:
        return Result.err(current_ret.err_value)

    new_tags: list[SearchTag] = []
    for tag in tags:
        tag_ret = SearchTag.new(sequence=tag.sequence, name=tag.name)
        if tag_ret.is_err:
            return Result.err(tag_ret.err_value)
        new_tags.append(tag_ret.ok_value)

    current = current_ret.ok_value
    updated_ret = current.update(tuple(new_tags))
    if updated_ret.is_err:
        return Result.err(updated_ret.err_value)

    updated = updated_ret.ok_value
    return atomic_result(lambda: save_search_tag_data(current.delete_ids(updated), updated))
```

※ `error.searchTagDuplicate`・`error.searchTagNameLength` は説明のための仮のキーで、FE の i18n にはまだない（`error.searchTagLimit` はある）。

### 要点
- **作る入り口を `_new` に集める**: `new`（新しく作る）も `update`（変える）も最後は `_new` を通るので、どこから作っても `_validate` が走る
- **frozen な dataclass にする**: 外から書き換えられないので、作ったあとに `_validate` を通らない値へ変わることがない。値を変えるときは `replace` で新しいオブジェクトを作る
- **決まりを持つ場所を分ける**: 1 つの検索タグの決まり（名前の長さ）は `SearchTag._validate`、まとめたときの決まり（数・重複）は `SearchTags._validate`
- **変え方の決まりは `update` に書く**: 「名前が同じなら id を引き継ぐ」のように、今の値と新しい値を比べる決まりは `_validate` ではなく `update` で扱う（`_validate` は作ったあとの値しか見ない）

### 弱いところ
- `SearchTags(...)` や `replace(...)` で直接作れるので、`_validate` を通らない作り方を型では防げない
- 確かめる決まりがないうちは `_validate` が `Result.ok(None)` だけになり、書く量だけ増える

## MyUs の今の作りとの対応

### 検索タグ（CRUD）

| パターン | MyUs の今の作り |
|---|---|
| `SearchTags` / `SearchTag`（データ + メソッド） | `domain/interface/search_tag/data.py` の `SearchTagData`（`@dataclass(frozen=True, slots=True)`）。メソッドは持たず、まとめる型もない |
| `SearchTags._validate` の数の上限 | `usecase/search_tag/core.py` の `update_search_tags` で `len(tags) > SEARCH_TAG_MAX_COUNT` を確かめる |
| `SearchTag._validate` の名前の長さ | `types/schema/user.py` の `SearchTagIn` で `Field(max_length=30)`（adapter の入力で確かめる）。空文字は確かめていない |
| `SearchTags._validate` の重複 | **確かめていない**。`name_map` は名前が重複しない前提で作っている |
| `SearchTags.update` の id の引き継ぎ | `update_search_tags` の中で `name_map` から `existing_id` を取り、`keep_ids` から `delete_ids` を出す |
| 名前の決まりを確かめる関数 | ハッシュタグは `usecase/hashtag/_convert.py` の `validate_name`（長さ・使える文字・NG ワード）が近い |

### サブスクリプション（状態遷移）

状態が変わるエンティティでは、`update` の代わりに `set_active`・`set_ended` のような遷移のメソッドを持ち、「今の状態から変われるか」をそこで確かめる。MyUs のサブスクリプションは Event Sourcing で作っていて、これを分けて持っている。

| パターン | MyUs の今の作り |
|---|---|
| 状態ごとに分けた型 | `domain/aggregate/subscription/state.py` の `SubscriptionState = IncompleteSubscription \| ActiveSubscription \| PastDueSubscription \| EndedSubscription` |
| 遷移のメソッドの「変われるか」の判断 | `decide.py` の `accept_provider_state`・`request_cancellation` で `match state` し、出すイベントを決める。だめなら `ValidationError` |
| 遷移のメソッドの「新しい状態を作る」 | `apply.py` の `apply` で `match state, envelope.event` し、イベントから次の状態を作る。ありえない組み合わせは `HistoryCorruptedError` |
| `_validate` | **ない**。期間・金額は決済サービスから来る値をそのまま信じている |

### まとめ
- パターンは「決まりを確かめる」と「データを持つ」を 1 つのクラスでやる。MyUs は「データ（dataclass）と、判断する関数（usecase / `decide`）を分ける」作りなので、dataclass にメソッドとして `_validate` を足すと層の決まりとぶつかる
- MyUs では決まりが adapter の入力（`SearchTagIn`）と usecase に散らばっていて、重複のように誰も確かめていない決まりもある

## MyUs で使うときの形

次の両方を満たす場面が出てきたら取り入れる。

1. 複数のフィールド・複数のデータにまたがる不変条件がある（例: 検索タグの数・名前の重複）
2. そのデータを作る経路がいくつもあり、それぞれで確かめると漏れが出る

そのときもクラスにメソッドとして持たせず、Data はそのままにして、**ルールを確かめてから Data を作る関数を domain に置く**。

### 置き場所

ルールは domain の外（adapter・usecase）に置かない。Event Sourcing でない集約も、`domain/aggregate/<集約>/decide.py` に置く。

| ファイル | 置くもの |
|---|---|
| `domain/aggregate/<集約>/decide.py` | ルールを確かめて、保存する Data を決める関数。I/O を持たない |
| `domain/interface/<集約>/data.py` | Data（今のまま。メソッドは持たない） |
| `usecase/<集約>/core.py` | 取得 → `decide.py` の関数 → 保存の段取りだけ。ルールは持たない |

- `decide.py` は interface（Data）と utils だけを import する。adapter の型（`SearchTagIn` などの schema）は受け取らず、usecase で Data に詰め替えてから渡す
- adapter の schema（`Field(max_length=30)` など）は入力の形を確かめるものとして残してよい。ただし同じルールを domain でも必ず確かめる
- `docs/backend.md` の層の表では、`domain/aggregate` は Event Sourcing の集約だけになっている。この形を取り入れるときは、表を「集約のルール（Event Sourcing の集約は `state.py`・`event.py`・`decide.py`・`apply.py`）」に広げる

### 検索タグの例

`domain/aggregate/search_tag/decide.py`

```python
from dataclasses import replace
from api.src.domain.interface.search_tag.data import SearchTagData
from api.utils.common.result import Result, ValidateError, ValidationError


SEARCH_TAG_MAX_COUNT = 20
SEARCH_TAG_NAME_MAX_LENGTH = 30


def replace_search_tags(current: list[SearchTagData], tags: list[SearchTagData]) -> Result[list[SearchTagData], ValidateError]:
    if len(tags) > SEARCH_TAG_MAX_COUNT:
        return Result.err(ValidationError("error.searchTagLimit"))

    names = [tag.name for tag in tags]
    sequences = [tag.sequence for tag in tags]
    if len(names) != len(set(names)) or len(sequences) != len(set(sequences)):
        return Result.err(ValidationError("error.searchTagDuplicate"))

    if any(len(name) == 0 or len(name) > SEARCH_TAG_NAME_MAX_LENGTH for name in names):
        return Result.err(ValidationError("error.searchTagNameLength"))

    id_map = {obj.name: obj.id for obj in current}
    return Result.ok([replace(tag, id=id_map.get(tag.name, 0)) for tag in tags])


def select_delete_ids(current: list[SearchTagData], updated: list[SearchTagData]) -> list[int]:
    keep_ids = {obj.id for obj in updated}
    return [obj.id for obj in current if obj.id not in keep_ids]
```

`usecase/search_tag/core.py`

```python
@Result.shield_exception()
def update_search_tags(author_id: int, tags: list[SearchTagIn]) -> Result[None, ValidateError]:
    current_ret = get_search_tag_data(author_id)
    if current_ret.is_err:
        return Result.err(current_ret.err_value)

    current = current_ret.ok_value
    new_tags = [SearchTagData(id=0, author_id=author_id, sequence=tag.sequence, name=tag.name) for tag in tags]
    updated_ret = replace_search_tags(current, new_tags)
    if updated_ret.is_err:
        return Result.err(updated_ret.err_value)

    updated = updated_ret.ok_value
    delete_ids = select_delete_ids(current, updated)
    save_ret = atomic_result(lambda: save_search_tag_data(delete_ids, updated))
    if save_ret.is_err:
        return Result.err(save_ret.err_value)

    return Result.ok(None)
```

- 1 つのデータのルール（名前の長さ）と、まとめたときのルール（数・重複）を `decide.py` の 1 つの関数で確かめる
- usecase から `SEARCH_TAG_MAX_COUNT` と `name_map` の処理がなくなり、取得・判断・保存の段取りだけになる
- `decide.py` は I/O を持たないので、Data を渡すだけで DB なしにテストできる
- 確かめるルールがないデータには作らない（中身が空の関数は置かない）

### 別案: usecase の `_convert.py` に置く

ルールの関数を domain ではなく、usecase の `_convert.py`（ハッシュタグの `validate_name` と同じ場所）に置く形。

- 置き場所: Event Sourcing の集約なら `domain/aggregate/<集約>/`、それ以外は usecase の `_convert.py`
- 呼ぶ側は Data を直接作らず、この関数を通して `is_err` なら返す

`usecase/search_tag/_convert.py`

```python
SEARCH_TAG_MAX_COUNT = 20
SEARCH_TAG_NAME_MAX_LENGTH = 30


def convert_search_tags(author_id: int, current: list[SearchTagData], tags: list[SearchTagIn]) -> Result[list[SearchTagData], ValidateError]:
    if len(tags) > SEARCH_TAG_MAX_COUNT:
        return Result.err(ValidationError("error.searchTagLimit"))

    names = [tag.name for tag in tags]
    sequences = [tag.sequence for tag in tags]
    if len(names) != len(set(names)) or len(sequences) != len(set(sequences)):
        return Result.err(ValidationError("error.searchTagDuplicate"))

    if any(len(name) == 0 or len(name) > SEARCH_TAG_NAME_MAX_LENGTH for name in names):
        return Result.err(ValidationError("error.searchTagNameLength"))

    id_map = {obj.name: obj.id for obj in current}
    return Result.ok([SearchTagData(id=id_map.get(tag.name, 0), author_id=author_id, sequence=tag.sequence, name=tag.name) for tag in tags])
```

- 1 つのデータのルール（名前の長さ）と、まとめたときのルール（数・重複）を 1 つの関数で確かめる
- 確かめるルールがないデータには作らない（中身が空の関数は置かない）

### domain に置く形と別案の比べ方

| 観点 | domain に置く形 | 別案（usecase の `_convert.py`） |
|---|---|---|
| ルールの置き場所 | domain に集まる。クリーンアーキテクチャの考え方に合う | usecase に残る |
| 受け取る型 | Data だけ。usecase で詰め替える手間がある | adapter の `SearchTagIn` をそのまま受け取れる |
| `docs/backend.md` の変更 | `domain/aggregate` の範囲を広げる必要がある | 今の決まりのままでよい |
| 向いている場面 | ルールが多い、ほかの usecase からも同じルールを使う | ルールが少なく、1 つの usecase でしか使わない |

## media（マンガ）でやった場合

検索タグは 1 つの usecase でしか作らないが、media は「作る（`usecase/media/core.py`）」と「管理画面で変える（`usecase/manage/media/core.py`）」の 2 つの経路がある。経路がいくつもあるので、このパターンが効きやすい。例にはマンガ（`ComicData`）を使う。

マンガは、ほかの media と集約の形が違う。

- ほかの media（video・music・blog・picture・chat）は、1 つのテーブルで完結する
- マンガは、親の `Comic` と子の `ComicPage`（`db/models/media.py`）の 2 つのテーブルを 1 つの集約として扱う。repository（`domain/entity/media/comic/repository.py`）は、`Comic` と一緒に `ComicPage` を `bulk_create` で保存し、取得するときは `sequence` の順に読む
- 親子をまとめたときのルール（ページは 1 枚以上）と、変え方のルール（更新ではページを変えられない）がある

親子のルールを集約のどこで守るかを示せるので、このパターンの例に一番向いている。

### 今の作り

| ルール | 今確かめている場所 |
|---|---|
| チャンネルの持ち主だけが作れる・変えられる | `create_comic`（`ForbiddenError("Forbidden")`）と `update_manage_comic`（`ForbiddenError("error.saveFailed")`）の 2 か所。ほかの media の作成・更新にも同じチェックがある |
| タイトルは 100 文字まで | adapter の schema（`types/schema/common.py` の `Title`）だけ |
| ページは 1 枚以上 | adapter の `pages: list[UploadedFile] = File(...)` で受け取るだけで、枚数は確かめていない |
| 更新ではページを変えられない | repository の `bulk_save` が新しく作ったマンガのページしか保存しないので、結果としてそうなっている。ルールとしてはどこにも書かれていない（次の「今の集約の形」を参照） |
| カテゴリは必ず要る | `create_comic` と `update_manage_comic` の 2 か所（`get_category_data` が `None` なら `ValidationError`） |
| 画像ファイルの形式・大きさ | `utils/functions/media.py` の `validate_uploads`（ファイルの中身を読む） |

- 同じルールが作成と更新の 2 か所に書かれていて、片方だけ直すと食い違う
- 同じ持ち主のチェックでも、エラーの文言が `"Forbidden"` と `"error.saveFailed"` で食い違っている
- 「ページは 1 枚以上」「更新ではページを変えられない」はルールとしてどこにも書かれていない

### 今の集約の形

recustomer の `CustomFieldQuestion`（親）と `FieldDetailQuestion`（子のエンティティ）と比べると、MyUs のマンガは**保存・読み込みは集約ルート経由になっているが、domain ではページが子のエンティティになっていない**。

集約ルート経由になっているところ（repository・DB）:

- `ComicPage` 専用の repository はなく、`ComicRepository` だけが `Comic` と `ComicPage` を一緒に扱う
- `bulk_save` は `transaction.atomic()` の中で `Comic` を保存し、続けて `ComicPage` を `bulk_create` する
- 取得は `Prefetch` で `ComicPage` を `sequence` の順にまとめて読む
- `ComicPage` の外部キーは `on_delete=CASCADE` なので、`Comic` を消すとページも消える

recustomer と違うところ（domain）:

| 観点 | recustomer（`CustomFieldQuestion`） | MyUs（`ComicData`） |
|---|---|---|
| 子の型 | `FieldDetailQuestion`（id・`_validate`・`update` を持つ子のエンティティ） | `pages: list[str]`。画像のパスが並んでいるだけで、ページの id も `sequence` も持たない |
| 子のルール | 子が自分の `_validate` で確かめる | ない |
| 親子をまとめたときのルール | 親の `_validate` で「詳細は 1 つ以上」 | ない（ページ 0 枚でも作れる） |
| 変え方のルール | 親の `update` で「詳細の追加・削除はできない」をはっきり確かめる | repository の中に隠れている |

「更新ではページを変えられない」が repository に隠れているところ:

- `get_save_new_ids`（`domain/entity/index.py`）は、新しく作った行の id だけを返す
- `bulk_save` はその id のマンガのページだけを `bulk_create` するので、更新のときに `ComicData.pages` を変えて渡しても、エラーにならずに黙って無視される
- 今は `update_manage_comic` が `pages` を変えないので困らないが、ページを変える機能を足すとここでつまずく
- `convert_data` は画像のパスが空のページを読み飛ばす（`if p.image.name`）ので、保存されているページの数と `pages` の数が食い違うことがある

### パターンの形で書くと

`Comic` 自身が `_validate` を持ち、作成（`new`）と更新（`update`）が必ずそれを通る。

```python
@dataclass(frozen=True, slots=True)
class Comic:
    data: ComicData

    def _validate(self) -> Result[None, ValidateError]:
        if len(self.data.title) > _TITLE_MAX_LENGTH:
            return Result.err(ValidationError("error.titleLength"))
        if len(self.data.pages) == 0:
            return Result.err(ValidationError("error.comicPageRequired"))
        return Result.ok(None)

    @classmethod
    def _new(cls, data: ComicData) -> Result[Comic, ValidateError]:
        obj = cls(data=data)
        if (ret := obj._validate()).is_err:
            return Result.err(ret.err_value)
        return Result.ok(obj)

    @classmethod
    def new(cls, user_id: int, channel: ChannelData, title: str, content: str, image: str, pages: list[str], publish: bool, publish_at: datetime) -> Result[Comic, WriteError]:
        if channel.owner_id != user_id:
            return Result.err(ForbiddenError("Forbidden"))
        return cls._new(ComicData(id=0, ulid="", title=title, content=content, image=image, pages=pages, read=0, like=0, publish=publish, publish_at=publish_at, created=datetime.min, updated=datetime.min, category_ulid="", channel=channel, hashtags=[]))

    def update(self, user_id: int, title: str, content: str, image: str, publish: bool, publish_at: datetime) -> Result[Comic, WriteError]:
        # ページは更新では変えられないので、引数に取らない
        if self.data.channel.owner_id != user_id:
            return Result.err(ForbiddenError("Forbidden"))
        return Comic._new(replace(self.data, title=title, content=content, image=image, publish=publish, publish_at=publish_at))
```

### MyUs で使うときの形（domain に置く）

`ComicData` はそのままにして、ルールを `domain/aggregate/comic/decide.py` の関数に集める。作成と更新の usecase は、どちらもこの関数を通す。

`domain/aggregate/comic/decide.py`

```python
from dataclasses import replace
from datetime import datetime
from api.src.domain.interface.channel.data import ChannelData
from api.src.domain.interface.media.comic.data import ComicData
from api.utils.common.result import ForbiddenError, Result, ValidationError, WriteError


COMIC_TITLE_MAX_LENGTH = 100


def create_comic(user_id: int, channel: ChannelData, title: str, content: str, image: str, pages: list[str], publish: bool, publish_at: datetime) -> Result[ComicData, WriteError]:
    if channel.owner_id != user_id:
        return Result.err(ForbiddenError("Forbidden"))

    comic = ComicData(id=0, ulid="", title=title, content=content, image=image, pages=pages, read=0, like=0, publish=publish, publish_at=publish_at, created=datetime.min, updated=datetime.min, category_ulid="", channel=channel, hashtags=[])
    return validate_comic(comic)


def update_comic(user_id: int, obj: ComicData, title: str, content: str, image: str, publish: bool, publish_at: datetime) -> Result[ComicData, WriteError]:
    if obj.channel.owner_id != user_id:
        return Result.err(ForbiddenError("Forbidden"))

    comic = replace(obj, title=title, content=content, image=image, publish=publish, publish_at=publish_at)
    return validate_comic(comic)


def validate_comic(comic: ComicData) -> Result[ComicData, WriteError]:
    if len(comic.title) > COMIC_TITLE_MAX_LENGTH:
        return Result.err(ValidationError("error.titleLength"))
    if len(comic.pages) == 0:
        return Result.err(ValidationError("error.comicPageRequired"))
    return Result.ok(comic)
```

`usecase/manage/media/core.py`（`usecase/media/core.py` の `create_comic` も同じ形になる）

```python
@Result.shield_exception()
def update_manage_comic(user_id: int, ulid: str, input: ComicUpdateIn, image: UploadedFile | None = None) -> Result[None, WriteError]:
    upload_ret = validate_uploads([(image, ImageUpload.COMIC)])
    if upload_ret.is_err:
        return Result.err(upload_ret.err_value)

    obj_ret = get_manage_comic(user_id, ulid)
    if obj_ret.is_err:
        return Result.err(obj_ret.err_value)

    obj = obj_ret.ok_value
    image_path = obj.image if image is None else save_upload(image, ImageUpload.COMIC, obj.channel.ulid)
    update_ret = update_comic(user_id, obj, input.title, input.content, image_path, input.publish, input.publish_at)
    if update_ret.is_err:
        return Result.err(update_ret.err_value)

    update_data = update_ret.ok_value
    category_data_ret = get_category_data(input.category_ulid)
    ...
```

- 持ち主・タイトルの長さ・ページの枚数のルールが `decide.py` の 1 か所にまとまり、作成と更新で食い違わなくなる。エラーの文言もそろう
- 「更新ではページを変えられない」は、`update_comic` が `pages` を引数に取らないことで表す。検索タグの `update` と同じく、変え方のルールは更新の関数に書く
- 画像ファイルの形式・大きさ（`validate_uploads`）はファイルの中身を読むので、usecase に残す。保存したあとのパス（`str`）だけを `decide.py` に渡す
- カテゴリがあるかどうかは DB を見ないとわからないので、usecase に残す（`decide.py` は I/O を持たない）
- 持ち主のチェックはほかの media にもあるので、取り入れるなら `domain/aggregate/media/decide.py` に `check_owner(user_id, channel)` のような共通の関数を置き、各 media の `decide.py` から呼ぶ
- usecase の例は `get_manage_comic`（持ち主で絞って探す）で取得している。この形にすると、持ち主でないときのエラーは今の `ForbiddenError("error.saveFailed")` ではなく `NotFoundError` になる
- `error.titleLength`・`error.comicPageRequired` は説明のための仮のキーで、FE の i18n にはまだない

### 子のエンティティにする形（recustomer に寄せる）

ページを子のエンティティとして扱い、ページのルールも `decide.py` で確かめる。repository は確かめ済みの Data を保存するだけにして、ルールを持たせない。

`domain/interface/media/comic/data.py`

```python
@dataclass(frozen=True, slots=True)
class ComicPageData:
    id: int
    sequence: int
    image: str


@dataclass(frozen=True, slots=True)
class ComicData:
    id: int
    ...
    pages: list[ComicPageData]
    ...
```

`domain/aggregate/comic/decide.py`

```python
def validate_comic_page(page: ComicPageData) -> Result[ComicPageData, WriteError]:
    if len(page.image) == 0:
        return Result.err(ValidationError("error.comicPageRequired"))
    return Result.ok(page)


def validate_comic(comic: ComicData) -> Result[ComicData, WriteError]:
    if len(comic.title) > COMIC_TITLE_MAX_LENGTH:
        return Result.err(ValidationError("error.titleLength"))
    if len(comic.pages) == 0:
        return Result.err(ValidationError("error.comicPageRequired"))

    sequences = [page.sequence for page in comic.pages]
    if len(sequences) != len(set(sequences)):
        return Result.err(ValidationError("error.comicPageDuplicate"))

    for page in comic.pages:
        if (ret := validate_comic_page(page)).is_err:
            return Result.err(ret.err_value)
    return Result.ok(comic)


def update_comic(user_id: int, obj: ComicData, title: str, content: str, image: str, pages: list[ComicPageData], publish: bool, publish_at: datetime) -> Result[ComicData, WriteError]:
    if obj.channel.owner_id != user_id:
        return Result.err(ForbiddenError("Forbidden"))

    if {page.id for page in obj.pages} != {page.id for page in pages}:
        return Result.err(ValidationError("error.comicPageNotChangeable"))

    comic = replace(obj, title=title, content=content, image=image, pages=pages, publish=publish, publish_at=publish_at)
    return validate_comic(comic)
```

- 1 枚のページのルール（画像がある）は `validate_comic_page`、まとめたときのルール（1 枚以上・`sequence` が重複しない）は `validate_comic` で確かめる。recustomer の子の `_validate` と親の `_validate` の分け方と同じ
- 「更新ではページを変えられない」は、`update_comic` でページの id の集まりが変わっていないかを確かめる。recustomer の `update` の `old_ids != new_ids` と同じ形で、repository に隠れていたルールを domain に出す
- この形にすると、並び替えなど id を変えない更新は受け付けられる。ページの追加・削除は、別の関数（例: `add_comic_page`）でルールを決めてから足す
- repository の `bulk_save` は、新しく作ったマンガかどうかで分けず、`ComicPageData` をそのまま保存する形に直す
- `error.comicPageDuplicate`・`error.comicPageNotChangeable` は説明のための仮のキーで、FE の i18n にはまだない

## 更新履歴
- 2026-11-10: 初版作成
