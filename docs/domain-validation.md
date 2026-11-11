# ドメインのルール（`validate`）

[README](../readme.md) / [バックエンド](backend.md) / [アーキテクチャ](architecture.md)

目的は「DB に不正なデータを入れない」こと。画面に出すエラー（入力の確かめ・文言）は FE で扱い、BE のルールは画面向けにしない。決まりの一覧は `docs/backend.md` の「Validation（ドメインのルール）」に書く。

## 形

ルールは `domain/interface/<ドメイン>/validation.py` の `validate` に書き、repository の `bulk_save` が保存する前に必ず呼ぶ。usecase はルールについて何もしない。

| ファイル | 置くもの |
|---|---|
| `domain/interface/<ドメイン>/validation.py` | ルールを確かめる関数 `validate`（1 つのファイルに複数あるときは `validate_xxx`）と、ルールに使う定数。I/O を持たない |
| `domain/interface/<ドメイン>/data.py` | Data（フィールドだけ。メソッドは持たない） |
| `domain/entity/<ドメイン>/repository.py` | `bulk_save` で保存する前に `validate` を呼ぶ。だめなら保存せずに `FatalError` を返す |
| `usecase/<ドメイン>/core.py` | 今までどおり `XxxData(...)`・`replace(...)` で Data を組み立てて保存する。ルールは持たない |

## マンガの例

`domain/interface/media/comic/validation.py`

```python
from api.src.domain.interface.media.comic.data import ComicData
from api.utils.common.result import Result, ValidationError


COMIC_TITLE_MAX_LENGTH = 100


def validate(obj: ComicData) -> Result[None, ValidationError]:
    if len(obj.title) > COMIC_TITLE_MAX_LENGTH:
        return Result.err(ValidationError("error.titleLength"))
    if len(obj.pages) == 0:
        return Result.err(ValidationError("error.pageRequired"))
    return Result.ok(None)
```

`domain/entity/media/comic/repository.py`

```python
@Result.shield_exception()
def bulk_save(self, objs: list[ComicData]) -> Result[list[int], FatalError]:
    if len(objs) == 0:
        return Result.ok([])

    errors = [ret.err_value.message for obj in objs if (ret := validate(obj)).is_err]
    if len(errors) > 0:
        return Result.err(FatalError(f"Invalid Data: {errors}"))
    ...
```

- usecase・コマンドなど、どの経路から保存しても `bulk_save` を通るので、必ずルールを通る。`ComicData(...)`・`replace(...)` で直接作っても、保存するときに止まる
- ここで止まるのは FE をすり抜けた不正なリクエストかバグのときだけなので、`FatalError`（500）でよい。Interface の `Result[T, FatalError]` の決まりもそのまま
- エラーの文言は media（ドメイン）ごとに分けず、`error.titleLength`・`error.pageRequired` のように共通にする。画面には出さない（BE のログにだけ出る）ので、FE の i18n には足さない
- DB から読むとき（entity の `convert_data`）は確かめないので、ルールを満たさない既存のデータがあっても読み込みは止まらない

## `__post_init__`・ファクトリで確かめない理由

「Data を作るとき（`__post_init__` やファクトリ）に確かめれば、保存時に確かめなくてよい」という形もあるが、MyUs では使わない。

- 組み立てる経路をわざと塞いでいない。Data はフィールドだけを持ち、usecase が `XxxData(...)`・`replace(...)` で自由に組み立てる。どの経路からでも必ず通るのは `bulk_save` だけなので、ここで確かめるのは二重のチェックではなく、ただ 1 つのチェックになる
- 守りたいのは書き込み（DB に不正なデータを入れない）で、読み込みは止めない。`__post_init__` で確かめると entity の `convert_data` でも止まり、ルールを満たさない既存の行が 1 つあるだけで画面ごと落ちる
- `__post_init__` は例外で止めることになり、エラーを `Result` で返す決まりと合わない。Data にメソッドを持たない決まりにも反する
- テストの偽物（`tests/fakes.py` など）で一部のフィールドだけを埋めた Data も作れなくなる

`PositiveMoney` のように、正しくない値を型で表せなくする形も今は使わない。同じ `Money` でも `CheckoutData`（0 円はだめ）と `SubscriptionData`（0 円もよい）で意味が違い、型を分けても得るものが少ないため。

## 状態遷移のルールとの分け方

| ルール | 置く場所 |
|---|---|
| 値のルール（長さ・範囲・必須など、保存する Data 1 つを見れば決まるもの） | `domain/interface/<ドメイン>/validation.py` の `validate` |
| 状態遷移のルール（「終わった状態からは遷移できない」など、今の状態と次の操作で決まるもの） | `domain/aggregate/<集約>/decide.py` |

- 状態遷移は `validate` で確かめない。サブスクリプション（`domain/aggregate/subscription`）は状態ごとに型を分け（`IncompleteSubscription`・`ActiveSubscription`・`PastDueSubscription`・`EndedSubscription`）、遷移してよいかは `decide.py` が決める
- `validate` のエラーのキーは判定と食い違わない名前にする。たとえば 0 を許す判定（`< 0` でだめ）に「正の値」を思わせる名前を付けない

## DB を見ないと決まらないルール

カテゴリがある・NG ワードを含まない・同じものがまだない、のように DB を読まないと確かめられないルールも、**ルールを持つのは domain** にする。DB を読む（判定に使う値を取ってくる）のは usecase・adapter でよい。

| 分けるもの | 置く場所 |
|---|---|
| ルール（何を満たせば通るか・だめなときに返すエラー） | domain（`domain/interface/<ドメイン>/validation.py`） |
| DB を読む処理 | usecase（`_convert.py` の `get_xxx_data`）と、その先の entity（adapter） |
| 読んだ値を渡してルールを呼ぶ段取り | usecase（`core.py`） |

- `validation.py` は I/O を持たないまま。DB を読んだ結果を引数で受け取って確かめる
- usecase は値を読んで渡すだけで、`if category_data is None:` のような判定やエラーのキーを書かない
- 作成と更新など経路がいくつあっても、同じ関数を通すので、ルールとエラーの文言が食い違わない

### 形 1: 読んだ値を渡す（基本）

usecase が DB から読んだ値（なければ `None`・一覧なら `list`）をそのまま `validation.py` の関数に渡し、domain が確かめる。

カテゴリ（今は `usecase/media/core.py`・`usecase/manage/media/core.py` の作成・更新 12 か所に `if category_data is None: return Result.err(ValidationError("error.categoryRequired"))` が書かれている）

`domain/interface/media/validation.py`

```python
from api.src.domain.interface.category.data import CategoryData
from api.utils.common.result import Result, ValidationError


def validate_category(category: CategoryData | None) -> Result[CategoryData, ValidationError]:
    if category is None:
        return Result.err(ValidationError("error.categoryRequired"))
    return Result.ok(category)
```

`usecase/media/core.py`

```python
category_data_ret = get_category_data(input.category_ulid)
if category_data_ret.is_err:
    return Result.err(category_data_ret.err_value)

category_ret = validate_category(category_data_ret.ok_value)
if category_ret.is_err:
    return Result.err(category_ret.err_value)

category_data = category_ret.ok_value
```

- 「あるかどうか」を確かめる関数は、戻り値を `Result[None, ValidationError]` ではなく、見つかった Data（`Result[CategoryData, ValidationError]`）にする。`None` を返すと usecase 側で `CategoryData | None` のままになり、もう一度 `None` を確かめることになるため

ハッシュタグの名前（今は `usecase/hashtag/_convert.py` の `validate_name` が NG ワードを受け取って確かめている）

- `get_ng_words_data`（DB を読む）は usecase の `_convert.py` に残す
- `validate_name`（長さ・使える文字・NG ワード）と `HASHTAG_MAX_LENGTH`・`ALLOWED_PATTERN` は `domain/interface/hashtag/validation.py` の `validate_name(name: str, ng_words: list[str]) -> Result[None, ValidationError]` に移す。引数の `ng_words` はそのままで、今の形がすでに「読んだ値を渡す」形になっている
- だめな名前はエラーにせず読み飛ばす今の動きは変えない。usecase は `is_err` なら `continue` する

### 形 2: Interface を渡す（探す条件そのものがルールのとき）

「同じチャンネルに同じ名前のものがまだない」のように、**どう探すか（FilterOption の条件）** がルールの中身になるときは、形 1 だと条件が usecase に残る。このときは `validation.py` の関数が Interface（ABC）を受け取り、探す条件も domain に書く。

```python
from api.src.domain.interface.xxx.interface import FilterOption, SortOption, XxxInterface
from api.utils.common.result import FatalError, Result, ValidationError


def validate_name_unused(repo: XxxInterface, channel_id: int, name: str) -> Result[None, ValidationError | FatalError]:
    ids_ret = repo.get_ids(FilterOption(channel_id=channel_id, name=name), SortOption(), limit=1)
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)
    if len(ids_ret.ok_value) > 0:
        return Result.err(ValidationError("error.nameDuplicate"))
    return Result.ok(None)
```

- 実際に DB を読むのは Interface の先の entity（adapter）。`validation.py` は Interface（同じ domain/interface）だけを import し、entity・injector は import しない。usecase が `injector.get(XxxInterface)` で取った repo を渡す
- テストでは Interface を満たす偽物を渡せば DB なしで確かめられる
- 探すのに使うメソッドは今ある `get_ids` と `FilterOption` の組み合わせにする。条件が足りないときは FilterOption に足す（ルール専用のメソッドを Repository に作らない）
- `validation.py` が I/O を持つことになるので、形 1 で書けるときは形 1 にする。今の MyUs にはこの形が要るルールはまだない（`error.nameDuplicate`・`XxxInterface` は説明のための仮の名前）。取り入れるときは `docs/backend.md` の「Validation」に「Interface を受け取ってよい」を足す

### DB の制約（UniqueConstraint など）との関係

- `subscribe` の `UniqueConstraint(fields=["user", "channel"])` のような DB の制約は、domain のルールをすり抜けたときの最後の守りとして残す
- 制約に引っかかったとき（`IntegrityError`）に adapter で `ValidationError` に変えて返す形にはしない。Interface は `Result[T, FatalError]` を返す決まりなので、ルールとして利用者に返すエラーは domain の関数（形 1・形 2）で先に確かめる

## 更新履歴
- 2026-11-11: `__post_init__`・ファクトリで確かめない理由と、状態遷移のルール（aggregate の `decide.py`）との分け方を足す
- 2026-11-11: 作りが決まったので、検討の文章（`_validate`・`_new` のパターン、recustomer との比べ、マンガで試した形など）を消し、決まった形だけにする
- 2026-11-11: 関数名を `validate_data`（`validate_xxx_data`）から `validate`（`validate_xxx`）にする。ルールを `validation.py` の `validate` に書き、repository の `bulk_save` で保存する前に確かめる形を足す。マンガをこの形にした
- 2026-11-11: ルールの置き場所を `domain/aggregate/<集約>/decide.py` から `domain/interface/<ドメイン>/validation.py`（#1265 の決まり）にそろえる。usecase の `_convert.py` に置く別案は、domain に置くと決めたので消す
- 2026-11-10: DB を見ないと決まらないルールも domain が持つ形（読んだ値を渡す・Interface を渡す）を足す。マンガのカテゴリを usecase に残すとしていたところを直す
- 2026-11-10: 初版作成
