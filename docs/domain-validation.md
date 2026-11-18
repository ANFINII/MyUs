# ドメインのルール（`validate`）

[README](../readme.md) / [バックエンド](backend.md) / [アーキテクチャ](architecture.md)

目的は「DB に不正なデータを入れない」こと。画面に出すエラー（入力の確かめ・文言）は FE で扱い、BE のルールは画面向けにしない。決まりの一覧は `docs/backend.md` の「Validation（ドメインのルール）」に書く。

## 形

ルールは `domain/<ドメイン>/validation.py` の `validate` に書き、repository の `bulk_save` が保存する前に必ず呼ぶ。usecase はルールについて何もしない。

| ファイル | 置くもの |
|---|---|
| `domain/<ドメイン>/validation.py` | ルールを確かめる関数 `validate`（1 つのファイルに複数あるときは `validate_xxx`）と、ルールに使う定数。I/O を持たない |
| `domain/<ドメイン>/data.py` | Data（フィールドだけ。メソッドは持たない） |
| `adapter/outbound/db/<ドメイン>/repository.py` | `bulk_save` で保存する前に `validate` を呼ぶ。だめなら保存せずに `FatalError` を返す |
| `usecase/<ドメイン>/core.py` | 今までどおり `XxxData(...)`・`replace(...)` で Data を組み立てて保存する。ルールは持たない |

## マンガの例

`domain/media/comic/validation.py`

```python
from myus.domain.media.comic.data import ComicData
from myus.utils.common.result import Result, ValidationError


COMIC_TITLE_MAX_LENGTH = 100


def validate(obj: ComicData) -> Result[None, ValidationError]:
    if len(obj.title) > COMIC_TITLE_MAX_LENGTH:
        return Result.err(ValidationError("error.titleLength"))
    if len(obj.pages) == 0:
        return Result.err(ValidationError("error.pageRequired"))
    return Result.ok(None)
```

`adapter/outbound/db/media/comic/repository.py`

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

- `ComicData(...)`・`replace(...)` で直接作っても、保存するときに止まる

## Data 1 つでは決まらないルール（数・重複）

検索タグの「20 個まで」のように、保存する Data をまとめて見ないと決まらないルールだけは、`validate` が list を受け取る。`bulk_save` では 1 回だけ呼ぶが、書き方はマンガと同じ `errors` の形にそろえる。

`domain/search_tag/validation.py`

```python
SEARCH_TAG_MAX_COUNT = 20


def validate(objs: list[SearchTagData]) -> Result[None, ValidationError]:
    if len(objs) > SEARCH_TAG_MAX_COUNT:
        return Result.err(ValidationError("error.searchTagLimit"))
    return Result.ok(None)
```

`adapter/outbound/db/search_tag/repository.py`

```python
errors = [ret.err_value.message for ret in [validate(objs)] if ret.is_err]
if len(errors) > 0:
    return Result.err(FatalError(f"Invalid Data: {errors}"))
```

- `bulk_save` に渡す list が、ルールの対象をすべて含んでいるときだけ使える。検索タグは `update_search_tags` が作者の検索タグをすべて `bulk_save` に渡している
- 1 つのファイルに Data 1 つのルールもあるときは、list を受け取る方を `validate_xxx` にする。ハッシュタグは、名前の `validate(obj)` と、1 つのメディアに 20 個までの `validate_count(objs)` に分けている

## `__post_init__`・ファクトリで確かめない理由

「Data を作るとき（`__post_init__` やファクトリ）に確かめれば、保存時に確かめなくてよい」という形もあるが、MyUs では使わない。

- 組み立てる経路をわざと塞いでいない。Data はフィールドだけを持ち、usecase が `XxxData(...)`・`replace(...)` で自由に組み立てる。どの経路からでも必ず通るのは `bulk_save` だけなので、ここで確かめるのは二重のチェックではなく、ただ 1 つのチェックになる
- 守りたいのは書き込み（DB に不正なデータを入れない）で、読み込みは止めない。`__post_init__` で確かめると adapter/outbound/db の `convert_data` でも止まり、ルールを満たさない既存の行が 1 つあるだけで画面ごと落ちる
- `__post_init__` は例外で止めることになり、エラーを `Result` で返す決まりと合わない。Data にメソッドを持たない決まりにも反する
- テストの偽物（`tests/fakes.py` など）で一部のフィールドだけを埋めた Data も作れなくなる

`PositiveMoney` のように、正しくない値を型で表せなくする形も今は使わない。同じ `Money` でも `CheckoutData`（0 円はだめ）と `SubscriptionData`（0 円もよい）で意味が違い、型を分けても得るものが少ないため。

## 状態遷移のルールとの分け方

| ルール | 置く場所 |
|---|---|
| 値のルール（長さ・範囲・必須など、保存する Data 1 つを見れば決まるもの。数・重複は Data の list） | `domain/<ドメイン>/validation.py` の `validate` |
| 状態遷移のルール（「終わった状態からは遷移できない」など、今の状態と次の操作で決まるもの） | `domain/<ドメイン>/<集約>/decide.py` |

- 状態遷移は `validate` で確かめない。サブスクリプション（`domain/payment/subscription`）は状態ごとに型を分け（`IncompleteSubscription`・`ActiveSubscription`・`PastDueSubscription`・`EndedSubscription`）、遷移してよいかは `decide.py` が決める
- `validate` のエラーのキーは判定と食い違わない名前にする。たとえば 0 を許す判定（`< 0` でだめ）に「正の値」を思わせる名前を付けない

## DB を見ないと決まらないルール

NG ワードを含まない・同じものがまだない、のように DB を読まないと確かめられないルールも、**ルールを持つのは domain** にする。DB を読む（判定に使う値を取ってくる）のは usecase・adapter でよい。

| 分けるもの | 置く場所 |
|---|---|
| ルール（何を満たせば通るか・だめなときに返すエラー） | domain（`domain/<ドメイン>/validation.py`） |
| DB を読む処理 | usecase（`_convert.py` の `get_xxx_data`）と、その先の repository（adapter/outbound/db） |
| 読んだ値を渡してルールを呼ぶ段取り | usecase（`core.py`） |

- `validation.py` は I/O を持たないまま。DB を読んだ結果を引数で受け取って確かめる
- usecase は値を読んで渡すだけで、判定やエラーのキーを書かない
- 作成と更新など経路がいくつあっても、同じ関数を通すので、ルールとエラーの文言が食い違わない
- リクエストにある参照先（カテゴリ・チャンネルの ulid など）を探して見つからないのは、ルールではない。`validation.py` には置かず、探す関数（`get_xxx_data`）で扱う。カテゴリは FE が必ず選ばせていて見つからないことはないので、`get_category_data` が見つからなければ `FatalError` を返す

### 読んだ値を渡す

usecase が DB から読んだ値（なければ `None`・一覧なら `list`）をそのまま `validation.py` の関数に渡し、domain が確かめる。

ハッシュタグの名前

- 長さ・使える文字（`HASHTAG_MAX_LENGTH`・`ALLOWED_PATTERN`）は、もう `domain/hashtag/validation.py` の `validate` にあり、repository の `bulk_save` が呼んでいる
- NG ワードは、今も `usecase/hashtag/_convert.py` の `has_ng_word` が `get_ng_words_data` で読んだ NG ワードを受け取って確かめている。この形にするなら、`has_ng_word` を `domain/hashtag/validation.py` の `validate_ng_word(name: str, ng_words: list[str]) -> Result[None, ValidationError]` に移し、`get_ng_words_data` は usecase の `_convert.py` に残す
- だめな名前はエラーにせず読み飛ばす今の動きは変えない。usecase は `is_err` なら `continue` する

### DB の制約（UniqueConstraint など）との関係

- `subscribe` の `UniqueConstraint(fields=["user", "channel"])` のような DB の制約は、domain のルールをすり抜けたときの最後の守りとして残す
- 制約に引っかかったとき（`IntegrityError`）に adapter で `ValidationError` に変えて返す形にはしない。Interface は `Result[T, FatalError]` を返す決まりなので、ルールとして利用者に返すエラーは domain の関数で先に確かめる
