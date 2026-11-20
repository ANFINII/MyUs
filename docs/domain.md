# ドメイン

[README](../readme.md) / [バックエンド](backend.md) / [アーキテクチャ](architecture.md)

`myus/myus/domain/` の決まり。domain はドメインごとのディレクトリに、Data・Interface・ルール・集約を置く。ほかの層には依存せず、I/O を持たない。

## ファイルの置き方

| ファイル | 置くもの |
|---|---|
| `domain/<ドメイン>/data.py` | Data。フィールドだけを持ち、メソッドを持たない |
| `domain/<ドメイン>/interface.py` | Repository の Interface と、検索の条件 `FilterOption`・`SortOption`・`PageOption`・`SortType` |
| `domain/<ドメイン>/validation.py` | 保存する前に確かめるルール `validate` と、ルールに使う定数 |
| `domain/<ドメイン>/<集約>/` | Event Sourcing の集約。`state.py`・`event.py`・`decide.py`・`apply.py` に分ける |
| `domain/media/common.py` | メディアに共通の検索の条件と定数。`MEDIA_PAGE_SIZE`・`MEDIA_TITLE_MAX` など |
| `domain/payment/plan.py` | 料金プラン。表ではなくコードの定数で持つ |

- `validation.py` は、確かめるルールがないドメインには作らない
- 集約は今は `domain/payment/subscription/` だけ。`aggregate/aggregate.py` のような1つのファイルや、いろいろな型を混ぜた `data.py` にしない
- 外部サービスとやりとりする実装は domain に置かず、`adapter/outbound/<外の相手>/` に置く。domain には Interface と、やりとりする Data だけを置く。決済は `domain/payment/provider/` の Interface を `adapter/outbound/payment/stripe/` が実装する
- DB に触れない処理、たとえばキャッシュには Interface を作らず、`utils/functions` の関数にする

## import

- domain は Data・ほかのドメインの Data と定数・`utils` だけを import する。usecase・adapter・injector・Django を import しない
- 同じドメインの中は相対パス、ほかの層は `myus.` から始まる絶対パスにする
- `utils` は domain を import しない。domain に触れる補助の関数は、usecase の `_convert.py` に置く

## Data

- `@dataclass(frozen=True, slots=True)` にし、名前は `Data` で終える。入力や結果の型も `SellerOnboardData`・`CheckoutCreatedData` のように `Data` で終える。`Data` を付けないのは、`db/models/` の Django のモデルだけ
- フィールドに初期値を付けない
- フィールドは、値の項目を先に、ほかの Data を持つ項目を後に、`None` になりうる項目をさらに後に並べる。作るときの引数も同じ順にする
- メソッドを持たない。ルールは `validation.py` に、判断は集約の `decide.py` に書く

## Interface

雛形は `domain/search_tag/interface.py`。新しく足すときも、今ある Interface と同じ名前・引数・戻り値にそろえ、独自の形を作らない。

| メソッド | 決まり |
|---|---|
| `get_ids(filter, sort, page)` | 必ず置く。条件に合う ID を返す |
| `bulk_get(ids)` | 必ず置く。ID の順に Data を返す |
| `bulk_save(objs)` | usecase で要るときだけ足す。保存する前に `validate` を呼ぶ |
| `bulk_delete(ids)` | usecase で要るときだけ足す |
| `count(filter)` | usecase で要るときだけ足す |

- 戻り値は `Result[T, FatalError]`。例外を投げない
- 使わないメソッドは足さない。いったん足したメソッドは、使わなくなっても消さない
- 条件で消す・取る専用のメソッド、たとえば `delete(type_no, object_id)` は作らない。`FilterOption` に条件を足し、`get_ids` で ID を取ってから `bulk_delete`・`bulk_get` する
- 今あるメソッドの組み合わせで足りるなら、新しいメソッドを足さない。足す前に確かめる
- `_` で始まる private メソッドを Interface に書かない
- `PageOption` の `limit` と `offset` の初期値は0で、上限なし。件数の上限がドメインで決まっているものだけ、その値にする。`search_tag` は `SEARCH_TAG_MAX_COUNT`、メディアは `MEDIA_PAGE_SIZE`

雛形と違う形を認めるのは、次の場合だけ。新しく足すときも、同じ種類の今ある形に合わせる。

- `bulk_save` で表せない更新：加算・切り替え・既読など。`save_read`・`save_count`・`save_follow_count`・`media_like`・`comment_like`、通知の `delete_by_user`・`confirm`
- 一覧に付ける判定：`is_liked`・`get_liked_ids`
- 認証：`UserInterface.authenticate`
- メディアの `SortOption`・`FilterOption`：スコア順で登録しているチャンネルの投稿を上げる `user_id`、詳細ページで今のメディアを外す `exclude_id`
- 広告の検索の条件：広告はメディアの種類ではないので、`domain/advertise/interface.py` に広告用を置く。`SortType` は `ID`・`CREATED` だけで、`FilterOption` に広告の種類の `advertise_type` を持つ
- カテゴリ・ハッシュタグの `bulk_save(media_type, media_id, objs)`：メディアへの紐づけの保存
- 外部サービスの窓口 `PaymentInterface`：DB のリポジトリではないので `get_ids`・`bulk_get` を持たない

## ルール

目的は、DB に不正なデータを入れないこと。画面に出すエラーは FE で扱い、BE のルールは画面向けにしない。

ルールは `validation.py` の `validate` に書き、repository の `bulk_save` が保存する前に必ず呼ぶ。usecase はルールについて何もしない。

- 名前は `validate`。1つのファイルに複数あるときは `validate_xxx` にする
- 引数は保存する Data、戻り値は `Result[None, ValidationError]`
- ルールに使う定数は同じ `validation.py` に置く。メディアに共通のものは `domain/media/common.py` に置く
- エラーのキーは、`error.titleLength`・`error.pageRequired` のようにドメインで分けず共通にする。判定と食い違う名前にしない。たとえば0を許す判定に「正の値」を思わせる名前を付けない
- 確かめるのは書き込みだけ。DB から読むとき、つまり adapter の `convert_data` では確かめない。ルールを満たさない古い行が1つあるだけで画面ごと落ちないようにするため
- `bulk_save` で止まるのは、FE をすり抜けた不正なリクエストかバグのときだけなので、`FatalError` で返してよい
- adapter の schema の `Field(max_length=...)` は、入力の形を確かめるものとして残してよい

### マンガの例

`domain/media/comic/validation.py`

```python
from myus.utils.common.result import Result, ValidationError
from .data import ComicData
from ..common import MEDIA_TITLE_MAX


def validate(obj: ComicData) -> Result[None, ValidationError]:
    if len(obj.title) > MEDIA_TITLE_MAX:
        return Result.err(ValidationError("error.titleLength"))

    if len(obj.pages) == 0:
        return Result.err(ValidationError("error.pageRequired"))

    if not 0 <= obj.free_pages < len(obj.pages):
        return Result.err(ValidationError("error.freePagesRange"))

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

`ComicData(...)` や `replace(...)` で直接作っても、保存するときに止まる。

### 数・重複のルール

検索タグの20個までのように、保存する Data をまとめて見ないと決まらないルールだけは、`validate` が list を受け取る。`bulk_save` では1回だけ呼び、書き方はマンガと同じ `errors` の形にそろえる。

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

- `bulk_save` に渡す list が、ルールの対象をすべて含んでいるときだけ使える。検索タグは、`update_search_tags` が作者の検索タグをすべて渡している
- Data 1つのルールもあるときは、list を受け取る方を `validate_xxx` にする。ハッシュタグは、名前の `validate(obj)` と、1つのメディアに20個までの `validate_count(objs)` に分けている

### DB を見ないと決まらないルール

NG ワードを含まない、同じものがまだない、のように DB を読まないと確かめられないルールも、ルールを持つのは domain にする。

| 分けるもの | 置く場所 |
|---|---|
| ルール。何を満たせば通るかと、だめなときのエラー | `domain/<ドメイン>/validation.py` |
| DB を読む処理 | usecase の `_convert.py` の `get_xxx_data` と、その先の repository |
| 読んだ値を渡してルールを呼ぶ段取り | usecase の `core.py` |

- `validation.py` は I/O を持たないまま、DB を読んだ結果を引数で受け取って確かめる
- usecase は値を読んで渡すだけで、判定やエラーのキーを書かない
- リクエストにある参照先、たとえばカテゴリやチャンネルの ulid が見つからないのはルールではない。探す関数 `get_xxx_data` で扱う。カテゴリは FE が必ず選ばせるので、`get_category_data` は見つからなければ `FatalError` を返す
- `subscribe` の `UniqueConstraint` のような DB の制約は、ルールをすり抜けたときの最後の守りとして残す。`IntegrityError` を adapter で `ValidationError` に変えて返す形にはしない

まだこの形になっていないもの：ハッシュタグの NG ワードは、今も `usecase/hashtag/_convert.py` の `has_ng_word` が確かめている。この形にするなら、`domain/hashtag/validation.py` の `validate_ng_word(name, ng_words)` に移す。だめな名前はエラーにせず読み飛ばす今の動きは変えない。

### プランで決まるルール

1時間以上のハイレゾは Premium 以上のように、ユーザーのプランで決まるルールは `validate` に入れない。保存する Data だけでは決まらないため。境の値は domain の定数にし、usecase がプランを読んで確かめる。

- 境の値：`domain/media/audio/validation.py` の `HIRES_LONG_SECONDS`
- プランの項目：`domain/payment/plan.py` の `Plan.is_long_hires`
- 確かめる所：`usecase/manage/media/core.py` の `update_manage_hires`

### Data を作るときに確かめない理由

`__post_init__` やファクトリで、Data を作るときに確かめる形は使わない。

- usecase は `XxxData(...)`・`replace(...)` で自由に Data を組み立てる。どの経路からでも必ず通るのは `bulk_save` だけなので、そこで確かめれば1回で済む
- `__post_init__` で確かめると、読み込みの `convert_data` でも止まり、古い行が1つあるだけで画面ごと落ちる
- 例外で止めることになり、エラーを `Result` で返す決まりと合わない。Data にメソッドを持たない決まりにも反する
- テストの偽物で、一部のフィールドだけを埋めた Data を作れなくなる

`PositiveMoney` のように、正しくない値を型で表せなくする形も今は使わない。同じ `Money` でも、`CheckoutData` は0円がだめで、`SubscriptionData` は0円もよい。型を分けても得るものが少ない。

## 集約

Event Sourcing の集約は、`domain/<ドメイン>/<集約>/` に置く。どれも I/O を持たない関数にする。

| ファイル | 置くもの |
|---|---|
| `state.py` | 状態の型。状態ごとに型を分ける。サブスクリプションは `IncompleteSubscription`・`ActiveSubscription`・`PastDueSubscription`・`EndedSubscription` |
| `event.py` | イベントの型 |
| `decide.py` | 今の状態と入力から、起こすイベントを決める。遷移してよいかもここで決める |
| `apply.py` | 状態にイベントを当てて次の状態を作る `apply` と、履歴から状態を作り直す `replay` |

- 値のルールは `validate`、状態遷移のルールは `decide.py` に置き、`validate` で状態遷移を確かめない

| ルール | 置く場所 |
|---|---|
| 値のルール。長さ・範囲・必須など | `validation.py` の `validate` |
| 状態遷移のルール。終わった状態からは遷移できない、など | 集約の `decide.py` |

- 集約の状態から画面が読む表を作る Projector は、usecase の `project_<集約>_data` に置く。反映した seq は `es_projection_progress` に、同じトランザクションで保存する
