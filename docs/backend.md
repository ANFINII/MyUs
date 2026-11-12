# バックエンド開発ルール

## 型ヒント

- Python 3.12+の型構文を使用（`list[str]`, `str | None`, `type`文）
- `Callable`は`collections.abc`からインポート
- すべての関数・メソッドに型ヒントを付与

## ロギング

- `print()`禁止、`myus.utils.common.logger`の`log`を使用
- 値はキーワード引数で構造化: `log.info("処理完了", user_id=123)`
- エラーログには`exc=e`を渡す

| レベル | 用途 |
|--------|------|
| `log.info()` | 処理の開始・完了、正常系ガード節 |
| `log.warning()` | 警告、軽度の異常系ガード節 |
| `log.error()` | エラー、危険度が高いガード節 |

## インポート

- ファイルの先頭で行う（ローカルインポート禁止、`TYPE_CHECKING`禁止）
- **`import X` 文は全て先頭にまとめる**（section に関係なく `from` より上）
  - 例: `import jwt` は `from dataclasses import replace` より上
- **`from X import Y` 文は section 順**: 標準ライブラリ → サードパーティ → Django → プロジェクト内（絶対パス）→ 同じ層の中（相対パス）
  - 各 section の中は、モジュールのパスの名前順に並べる（`myus.adapter` → `myus.db` → `myus.domain` → `myus.injectors` → `myus.usecase` → `myus.utils`）
- **同じ層の中の import は相対パスにする**: 層は `adapter/inbound`・`adapter/outbound`・`domain`・`usecase`・`injectors`・`utils`・`db`
  - 同じ層の中は `.`・`..` で書く（例: `usecase/media/core.py` から `from ._convert import ...`・`from ..category._convert import ...`・`from ..dto.media import ...`）
  - 層をまたぐものは `myus.` から始まる絶対パスで書く（例: usecase から `from myus.domain.media.video.data import VideoData`）
  - 相対パスは近いものから並べる（`.` → `..` → `...`。同じ深さの中は名前順）。FE の `import/order`（同じフォルダ → 親）に合わせる
  - パッケージの外（`config/`・`tests/`）からは絶対パスで書く
- **`from x import a, b, c` の中身は domain 順序を維持する**（alphabetical にしない）
  - 例: `from myus.db.models.media import Video, Music, Blog, Comic, Picture, Chat` は `MediaType` enum の定義順を保つ
- **`ruff check --fix` を勝手に実行しない**: ruff の isort 挙動は上記ルールと衝突するため、import 整理が必要なときは手動で対応する

## 命名規則

| 対象 | 規則 | 例 |
|------|------|-----|
| 変数・関数 | snake_case | `user_name`, `get_user()` |
| クラス | PascalCase | `VideoConverter` |
| 定数 | UPPER_SNAKE_CASE | `MAX_FILE_SIZE` |
| プライベート | 先頭に`_` | `_internal_method()` |
| Django Model | 単数形 | `User`, `Video` |

### `_data` の付く関数

`_data` は「Data（dataclass）を扱う関数」に付け、どの層の関数かは動詞で見分ける。

| 層 | 動詞 | injector | 例 |
|------|------|------|-----|
| adapter/outbound/db の `_convert.py` | `convert`（Model → Data）・`marshal`（Data → Model） | 使わない | `convert_data`・`marshal_data`、1つのファイルに複数あるときは `profile_data`・`marshal_profile_data` |
| usecase の補助の関数 | 取ってくるなら `get`、書き込むなら `create`（新しく作る）・`save`（保存・更新）・`delete`（消す） | 使う（Repository を通して読み書きする） | `get_user_data`・`create_video_data`・`save_comment_data`・`delete_video_data`・`save_access_data` |
| usecase の入口 | `get`・`create`・`update`・`delete` など | 使う | `get_user`・`create_video`（`_data` を付けない） |

- usecase の `_convert.py` で injector を使う関数（Repository を取り出す関数を通して使うものも含む）は、すべて `_data` で終える
- ただし Repository そのものを取り出す関数は、Data を扱わないので `get_xxx_repository` とし、`_data` を付けない（`get_media_repository`・`get_payment_repository`）
- Data 以外を変換する関数は `_data` を付けない（`convert_content`・`marshal_content`・`marshal_outbox`）

## 条件判定

- 空チェック: `len(items) == 0`（truthy判定は使わない）
- None判定: `is None` / `is not None`
- ブール値: 直接評価（`if enabled:`）
- 存在チェック: `in`演算子
- 型チェック: `isinstance()`

## return文

- 戻り値を変数として利用する場合: `return None`を明示
- ガード節・ループ脱出: `return`のみ
- 関数末尾: 戻り値を利用しない場合は省略

## enum変換

- `match-case`を使用
- 網羅性チェック: `assert_never`推奨

## リスト内包表記

- シンプルな変換のみ使用、複雑ならfor文

## 例外処理

- 素の`except:`や`except Exception:`でのキャッチは禁止（想定する例外型を明示する）
- やむを得ず広くキャッチする場合は`log.error`でスタックトレースを残す
- adapter層でのみHTTPステータスとエラーレスポンスを返す（usecase/domain層は`Result`で伝搬。次の「エラーハンドリング（Result型）」を参照）

## エラーハンドリング（Result型）

### Repository・usecase
- Interface・Repository・usecaseは`Result[T, E]`を返す（`from myus.utils.common.result import FatalError, NotFoundError, Result`）
- 公開メソッド・usecase関数には`@Result.shield_exception()`を付け、想定外の例外を`FatalError`に変換する
- Resultを受けたらその場で`is_err`を確認し、Errならそのまま返す
- 受け取る変数名: 関数内で受けるResultが1つなら`ret`、複数なら`ids_ret`・`follows_ret`のように`<名前>_ret`
- `injector.get`で取るRepositoryの変数名: その関数のメインのリソースのRepositoryは`repo`、ほかにもRepositoryを使うときは`category_repo`・`user_repo`のように`<名前>_repo`
  - 例: `create_video_data`は`repo`（動画）と`category_repo`、`save_follow_data`は`repo`（フォロー）と`user_repo`
  - 外部サービス（`PaymentInterface`）も同じ扱い（メインなら`repo`、ほかにメインがあれば`payment_repo`）
- `ok_value`は直接使わず、`ids = ids_ret.ok_value`のように1行で変数に取り出してから使う
- 複数の書き込みを1つのトランザクションにまとめるときは、書き込みを`Result`を返す関数に切り出し、`atomic_result`（`myus/utils/functions/transaction.py`）に渡す。関数がErrを返すとロールバックしてそのErrを返し、例外が出てもロールバックする（Errは例外ではないため、`transaction.atomic()`の中でErrを返すだけではロールバックされない）
  - 切り出す関数は、作成なら`create_xxx_data`、保存なら`save_xxx_data`、削除なら`delete_xxx_data`と名付け、`@Result.shield_exception()`を付ける。頭に`_`は付けない。置き場所は、似た関数があればその隣、無ければファイルの末尾にまとめる
  - usecaseで`with transaction.atomic():`と`transaction.set_rollback(True)`は使わない（`set_rollback`はruffの`TID251`で禁止している）

```python
save_ret = atomic_result(lambda: save_follow_data(follower, following, follow, is_follow))
if save_ret.is_err:
    return Result.err(save_ret.err_value)
```

```python
@Result.shield_exception()
def is_following(follower_id: int, following_id: int) -> Result[bool, FatalError]:
    follow_repo = injector.get(FollowInterface)
    ids_ret = follow_repo.get_ids(FollowFilterOption(follower_id=follower_id, following_id=following_id), FollowSortOption())
    if ids_ret.is_err:
        return Result.err(ids_ret.err_value)

    ids = ids_ret.ok_value
    if len(ids) == 0:
        return Result.ok(False)
    ...
```

### エラー型
- エラー型は`myus/utils/common/result/errors.py`の共通型を使う（usecaseごとの`errors.py`は作らない）
- 条件の意味で型を選ぶ（エンドポイントの種類では決めない）
- エラー型に`@final`は付けない

| エラー型 | 使う条件 | `type`（`ErrorType`） | HTTPステータス | message |
|---|---|---|---|---|
| `ValidationError` | 入力や業務ルールに反する（上限超過・ファイル形式等） | `VALIDATION` | 400 | `message` |
| `ForbiddenError` | 対象はあるが操作する権限がない（持ち主ではない等） | `FORBIDDEN` | 400 | `message` |
| `NotFoundError` | 対象が存在しない（`is None`・`len(ids) == 0`） | `NOT_FOUND` | 400 | `message` |
| `FatalError` | 想定外のエラー（DB・外部APIの例外等） | `INTERNAL` | 500 | `"Internal Server Error"`固定 |
| `ConflictError` | 同じ集約に同時に書き込み、取り直しても保存できなかった（イベントストア） | adapter で返すときに `CONFLICT` を足す | 400 | `message` |
| `HistoryCorruptedError` | 集約の履歴が壊れている（`seq` の抜け・未登録の種類・読めない中身）。再試行しても直らない | `INTERNAL` | 500 | `"Internal Server Error"`固定 |

- エラーレスポンスは`ErrorOut`（`type`・`message`）で返す（`myus/adapter/inbound/schema/common.py`）。`type`は必須
- 成功時に文言だけを返すときは`ErrorOut`ではなく`SuccessOut`（`message`）を使う
- `auth_check`（`myus/adapter/inbound/auth.py`。Cookieからトークンを取り出してusecaseの`verify_token`で確かめる）の結果が`None`（未ログイン）のときも`UNAUTHENTICATED`を返す
- HTTPステータスは成功が200、エラーが400 / 500だけを使う（201・204・401・403・404は使わない）。FEはステータスではなく`type`で出し分ける
- `response={...}`も`200`・`400: ErrorOut`・`500: ErrorOut`だけを書く（`response={...}`に無いステータスを返すとNinjaが実行時に例外にする）
- 成功で返すものが無いときは`200: None`・`return 200, None`にする

### エラー型の組み合わせ
- 複数のエラー型を返すときは、`NotFoundError | FatalError`のように直接書かず、`errors.py`の別名を使う
- `FatalError`だけのときは`Result[T, FatalError]`のまま書く
- 返すエラーが増減したら、合う別名に付け替える（付け替え忘れはadapterの`assert_never`でmypyが検出する）

| 別名 | 中身 | 使う場面 |
|---|---|---|
| `FindError` | `NotFoundError \| FatalError` | 対象を探す（見つからないことがある） |
| `AccessError` | `NotFoundError \| ForbiddenError \| FatalError` | 対象を探し、権限を確かめる |
| `InputError` | `NotFoundError \| ValidationError \| FatalError` | 対象を探し、入力を確かめる |
| `WriteError` | `NotFoundError \| ForbiddenError \| ValidationError \| FatalError` | 対象・権限・入力をすべて確かめて書き込む |
| `ValidateError` | `ValidationError \| FatalError` | 入力だけを確かめる |
| `HistoryError` | `HistoryCorruptedError \| FatalError` | 集約の履歴を読む |
| `AppendError` | `ConflictError \| FatalError` | 集約にイベントを追記する |
| `CommandError` | `ValidationError \| ConflictError \| HistoryCorruptedError \| FatalError` | コマンドを処理する（取得 → 判断 → 保存） |

```python
@Result.shield_exception()
def create_video(user_id: int, input: VideoIn, image: UploadedFile, video: UploadedFile) -> Result[MediaCreateDTO, WriteError]:
    ...
```

### adapter
- `FatalError`以外のエラー型も返すusecaseは、`match` + `assert_never`でエラー型ごとにステータスを決める（`isinstance`で分岐しない）
- usecaseに新しいエラー型が追加されたとき、adapterの対応漏れを`assert_never`でmypyが検出する
- `Result[T, FatalError]`だけを返すusecaseは`if ret.is_err: return 500, ...`のままでよい
- `case`はエラー型の表の上から順に並べ、最後を`case _: assert_never(...)`にする
- BEにしか表示されないメッセージ（500など）は英語にする
- 画面に出るエラーの文言は、日本語で書かずにFEのi18nのキー（`"error.loginFailed"`等）で返す（`ErrorOut`の`message`、エラー型の`message`とも）。FEが表示中の言語に翻訳する
- 新しいキーを使うときは、FEの`frontend/src/lib/i18n/locales/{ja,en}/common.json`の`error`に同じキーを追加する（無いキーはそのまま画面に出る）
- エラー型の`message`は`match`の前で`message = ret.err_value.message`と変数に取り出し、`ErrorOut(..., message=message)`で渡す（`message`が他の変数と被るときは`error_message`にする）

```python
ret = update_manage_video(user_id, ulid, input, image)
if ret.is_err:
    message = ret.err_value.message
    match ret.err_value:
        case ValidationError():
            return 400, ErrorOut(type=ErrorType.VALIDATION, message=message)
        case ForbiddenError():
            return 400, ErrorOut(type=ErrorType.FORBIDDEN, message=message)
        case NotFoundError():
            return 400, ErrorOut(type=ErrorType.NOT_FOUND, message=message)
        case FatalError():
            return 500, ErrorOut(type=ErrorType.INTERNAL, message="Internal Server Error")
        case _:
            assert_never(ret.err_value)
```

- 400以上のレスポンスは、ミドルウェア（`config/middleware.py`の`ErrorResponseLogMiddleware`）が`path`・`status`・`type`をログに出す
- Django本体のログは、`config/settings/base.py`の`LOGGING`でERROR以上（捕まえていない例外の500とトレースバック等）をコンソールに出す。400はミドルウェアが出すため、Django本体の`Bad Request`の警告は出さない
- `/api/`へのPOST・PUT・PATCH・DELETEは、ミドルウェア（`config/middleware.py`の`OriginCheckMiddleware`）が`Origin`ヘッダーを確かめ、`CSRF_TRUSTED_ORIGINS`に無いときは400（`FORBIDDEN`）を返す（CSRF対策。`Origin`が無いサーバー間の通信は通す）。FEのURLを変えたら`CSRF_TRUSTED_ORIGINS`も変える

## 文字列

- f-stringを使用（`.format()`や`%`は使わない）
- ただしログ出力ではf-stringを使わず、キーワード引数で渡す（ロギングセクション参照）

## 型定義

### アダプター（API）: Pydantic BaseModel
- 置き場所: `adapter/inbound/schema/`（adapter/inbound だけが使う。usecase からは import しない）
- サフィックス: 入力`In`、出力`Out`

### usecase の入出力: dataclass（`usecase/dto/`）
- `@dataclass(frozen=True, slots=True)`
- サフィックス: `DTO`
- 入力は`XxxDTO`にする（`SignupDTO`・`SettingProfileDTO`・`SearchTagDTO`）。項目はschemaの`XxxIn`と同じ名前にする
- 作成と更新で項目が違い、両方の入力があるときだけ`XxxCreateDTO`・`XxxUpdateDTO`に分ける（`VideoCreateDTO`・`VideoUpdateDTO`）。作成と更新で項目が同じなら1つの`XxxDTO`にする（`AdvertiseDTO`・`ChannelDTO`）
- `XxxDTO`がすでに出力などに使われているときは、`XxxCreateDTO`のように付けて分ける（`CommentDTO`があるので`CommentCreateDTO`）
- usecaseはschema（`XxxIn`）を受け取らない。adapterで`dto = VideoCreateDTO(**input.model_dump())`と組み替えて渡す
- 項目が1つだけなら、DTOを作らず値で渡す

### 内部データ構造: dataclass
- `@dataclass(frozen=True, slots=True)`
- サフィックス: `Data`
- domain interfaceのdataclassにはフィールドの初期値を設定しない
- dataclass はフィールドだけを持ち、メソッドを持たない。ルールは `validation.py` の `validate` に書き、repository の `bulk_save` が保存する前に呼ぶ（「Validation（ドメインのルール）」を参照）

## アーキテクチャ

### Repository層
- 入出力はdataclass（Django ORMモデルを直接返さない）
- usecase層ではinjector経由でinterfaceを取得（adapter/outbound の実装を直接インポートしない）

### Interface層（抽象クラス）
- **既存Interfaceの「シグネチャ・命名・構成」に必ず準拠**（独自設計禁止）
- 雛形: `myus/domain/search_tag/interface.py` を参照
- 必須メソッド: `get_ids(filter, sort, limit)` / `bulk_get(ids)` の読み取り2点
- 任意メソッド（usecaseで必要になったときに追加）: `bulk_save` / `bulk_delete` / `count`
- 必須型: `FilterOption` / `SortOption` dataclass + `SortType` enum
- メソッド追加時は既存パターンと **完全に同じシグネチャ・引数名** を使う（独自シグネチャ禁止）
- 「使わないから書く」「使うから簡略化する」のどちらも禁止：使う分だけ既存の形で書く
- 条件で消す・取る専用のメソッド（`delete(type_no, object_id, ...)` など）は作らない。`FilterOption`に条件を足し、`get_ids`で ID を取ってから`bulk_delete`・`bulk_get`する
- private メソッド（`_` プレフィックス）を Interface に宣言しない（抽象化は公開 API のみ。private ヘルパーは Repository 実装側に置く）
- 雛形と違う形を認めるのは次の場合だけ（新しく足すときも、同じ種類の既存の形に合わせる）
  - `bulk_save`で表せない更新：加算・切り替え・既読など（`save_read`・`save_count`・`save_follow_count`・`media_like`・`comment_like`、通知の`delete_by_user`・`confirm`）
  - 一覧に付ける判定：`is_liked`・`get_liked_ids`
  - 認証：`UserInterface.authenticate`
  - メディア・広告の`get_ids(filter, exclude, sort, page, user_id)`：ページング（`PageOption`）とスコア順の`user_id`が要るメディア共通の形。広告にはスコアがないので、`SortOption`・`SortType`（`ID`・`CREATED`）だけは`domain/advertise/interface.py`に広告用を置く
  - カテゴリ・ハッシュタグの`bulk_save(media_type, media_id, objs)`：メディアへの紐づけの保存
  - 外部サービスの窓口（`PaymentInterface`）：DBのリポジトリではないため`get_ids`・`bulk_get`を持たない

### Converterパターン
- `_convert.py`に変換関数を定義
- `convert_data`: Django ORM → dataclass
- `marshal_data`: dataclass → Django ORM
- 1つのファイルに複数あるときは `xxx_data`・`marshal_xxx_data`（例：`profile_data`・`marshal_profile_data`）
- 並び順は、`convert`系（Model → Data。`convert_data`・`xxx_data`・`convert_content`）→ `marshal`系（Data → Model）→ それ以外（`get_media_model`・`get_through_model`など）

### bulk操作
- `bulk_save`は`get_save_new_ids`（`myus/adapter/outbound/db/base.py`）で保存する
  - id未設定（`pk is None`）の行は`save(force_insert=True)`でINSERTし（IDはDBの自動採番）、既存の行は`bulk_create(update_conflicts=True)`でupsertする
  - 新しく振られたIDを返す。INSERTとupsertは`get_save_new_ids`の中で`transaction.atomic()`に入る
  - 関連テーブルなどと一緒に保存するときは、`get_save_new_ids`と関連テーブルの保存を`transaction.atomic()`で包む
- upsertの`update_fields`（`XXX_FIELDS`）
  - 閲覧数・件数などのカウンタは入れない（読み込んだ時点の古い値で上書きしてしまうため）。カウンタは`save_read`（`F("read") + 1`）や`save_count`のような専用のメソッドで、その項目だけを`QuerySet.update()`で書く
  - `updated`（`auto_now=True`）は入れる（入れないと、編集しても更新日が変わらない）
- IDを事前に採番しない（`ALTER TABLE ... AUTO_INCREMENT`はMySQLで暗黙にCOMMITされ、`transaction.atomic()`のロールバックが効かなくなるため）

```python
models = [marshal_data(o) for o in objs]
new_ids = get_save_new_ids(models, FOLLOW_FIELDS)

return Result.ok(new_ids)
```

## 層の責務

| 層 | 責務 | 依存してよいもの |
|------|------|------|
| adapter/inbound | HTTP・WebSocket のリクエスト/レスポンス変換、認証チェック。schema（`adapter/inbound/schema/`）を持つ | usecase, DTO |
| usecase | ビジネスロジック、複数repositoryの協調 | interface（injector経由） |
| domain/<ドメイン> | 抽象定義（ABC, dataclass）とルール（`validation.py`） | なし |
| domain/<ドメイン>/<集約> | Event Sourcing の集約（`state.py`・`event.py`・`decide.py`・`apply.py`）。I/O を持たない純粋な関数。いまは `domain/payment/subscription` | Data, utils |
| adapter/outbound/db | Repository の実装、DBアクセス | Django ORM, interface |
| adapter/outbound/payment | 決済会社（Stripe など）の Interface の実装 | interface, 外部の SDK |
| utils | どの層からも使う汎用の関数・定数・enum | なし（domain・injector・usecase を import しない） |

- adapter → usecase → interface の方向にのみ依存する
- usecase層からadapter層の型（`HttpRequest`、schemaの`XxxIn`等）をインポートしない。入力はadapterでDTOに組み替えて受け取る（「型定義」を参照）
- usecase層からDjangoのモデル（`User.objects`等）や`authenticate`を直接使わない。リポジトリ（Interface）のメソッドを通す
- domain層（`domain/<ドメイン>/`）は他の層に依存しない（純粋なPython）
- usecaseはドメインごとのディレクトリ（`usecase/<ドメイン>/`）にし、次の2つに分ける
  - `core.py`：adapter・コマンドから呼ぶ関数
  - `_convert.py`：補助の関数（`save_xxx_data`・`delete_xxx_data`、Repositoryを取り出す`get_media_repository`、ほかのusecaseから使う`create_notification_data`・`save_access_data`など）。補助の関数がなければ作らない
  - `_convert.py`は同じディレクトリの`core.py`をimportしない（`core.py`が`_convert.py`を使う向きだけにする）
  - adapter からも呼ぶ関数（`get_user_data`・`get_channel_data`・`get_search_tag_data`など）は、ほかの usecase から使っていても`core.py`に置く。adapter から呼ばないものだけを`_convert.py`に置く（`get_author_data`・`get_author_map_data`など）
- domainに触れる補助の関数は`utils`に置かず、usecaseの`_convert.py`に置く

## Validation（ドメインのルール）

目的は「DB に不正なデータを入れない」こと。画面に出すエラー（入力の確かめ・文言）は FE で扱い、BE のルールは画面向けにしない。

- データのルール（長さ・数など）は `domain/<ドメイン>/validation.py` の関数 `validate(obj)` に書く。adapter・usecase に置かない
  - 名前は `validate`（`_data` を付けない）。1 つのファイルに複数あるときは `validate_xxx` にする
  - 引数は保存する Data、戻り値は `Result[None, ValidationError]`
  - 数・重複のように Data 1 つでは決まらないルールだけは、`validate(objs)` で list を受け取る（例：検索タグの 20 個まで）
  - Data（`data.py`）はフィールドだけを持ち、メソッドを持たない
  - `validation.py` は Data と utils だけを import し、I/O を持たない
  - エラーの文言は media（ドメイン）ごとに分けず、`error.titleLength`・`error.pageRequired` のように共通にする。画面には出さない（BE のログにだけ出る）ので、FE の i18n には足さない
  - ルールに使う定数（`COMIC_TITLE_MAX_LENGTH` など）は同じ `validation.py` に置く
- repository の `bulk_save` は、保存する前に各 Data を `validate` に通し、だめなら保存せずに `FatalError` を返す
  - usecase・コマンドなど、どの経路から保存しても必ずルールを通る
  - Interface の `Result[T, FatalError]` の決まりはそのまま
  - ここで止まるのは FE をすり抜けた不正なリクエストかバグのときだけなので、500 で返してよい
- usecase は今までどおり `XxxData(...)`・`replace(...)` で Data を組み立てる。ルールを確かめる処理は書かない
- DB から読むとき（adapter/outbound/db の `convert_data`）は確かめない（読み込みは止めない）
- adapter の schema（`Field(max_length=...)`）は入力の形を確かめるものとして残してよい。DB に入れてよいかの判断は `validate` が持つ
- 確かめるルールがない Data には `validation.py` を作らない
- 例とDB を見ないと決まらないルールは [domain-validation.md](domain-validation.md) を参照

## パフォーマンス

- `select_related()`/`prefetch_related()`でN+1回避
- 必要なフィールドのみ`only()`で取得
- QuerySetは遅延評価されるため、評価タイミングを意識する

## テスト

- pytestを使用（Django TestCase不可）
- 今は決済など絶対に失敗できない箇所だけテストを書く（webhook・Stripeの署名の検証・退会時のサブスク解約・決済のイベントの反映）
- `@pytest.mark.django_db`でDB接続
- 実行: `uv run pytest`（`tests/`。CIでも実行する）
- テスト用DBは`--nomigrations`でモデルから直接作る（マイグレーションはgit管理外のため）。DBを作る権限のあるユーザーで実行する
- 共通のfixtureは`tests/conftest.py`
  - `make_user`: User・Profile・MyPage・UserNotification・UserPlanをまとめて作る
  - `fake_payment`: `PaymentInterface`を`tests/fakes.py`の`FakePayment`に差し替える（Stripeを呼ばない。テストごとに元に戻る）
- `PaymentEvent`の`content`（`PaymentEventContent`）と集約のイベント（`SUBSCRIPTION_EVENT_CLASSES`など）の形は、`tests/schema_compatibility/payment_event/*.json`・`es_event/*.json`に保存したJSONスキーマと比べて検査する（`test_schema_compatibility.py`）。比べる処理は`myus/utils/functions/schema_compatibility.py`、確かめるイベントの一覧は`export_event_schema`の`event_schemas`
  - 過去のイベントを読めなくなる変更（項目の削除・型の変更・必須の項目の追加・enumの値の削除）はテストが落ちる
  - 項目を足すときは初期値を付ける。形を変えたら`uv run python manage.py export_event_schema`でスキーマを書き出す（読めなくなる変更は書き出さない）
  - 保存したスキーマを手で直して検査を通さない

## リンターチェック（必須）

コードを書いた後、`myus/` で必ず実行:

```bash
uv run mypy myus config tests
uv run ruff check myus config tests --extend-ignore I
```

- ruff の `I`（import の並べ替え）は、上の「インポート」の決まりと合わないため除く
- lint の抑制コメント（`# noqa`）は書かない。外すときは例外を絞るか、`pyproject.toml` の `per-file-ignores` に書く

## 更新履歴
- 2025-09-29: 初版作成
- 2026-01-21: コーディング規約整理、型定義ルール変更
- 2026-02-04: Repository層ルール追加
- 2026-02-22: 全体整備、domain interface初期値禁止ルール追加
- 2026-04-16: docs/に一元化、構成整理
- 2026-10-20: エラーハンドリング（Result型・エラー型とHTTPステータスの対応・adapterのmatch + assert_never）を追加
- 2026-10-21: HTTPステータスを成功は200、エラーは400 / 500にまとめた
- 2026-10-21: 画面に出るエラーの文言をFEのi18nのキーで返すようにした
- 2026-10-21: CSRF対策として`OriginCheckMiddleware`を追加
- 2026-10-22: Interfaceで雛形と違う形を認める場合を追記
- 2026-11-08: `utils`はdomainに依存しないこと、domainに触れる補助の関数はusecaseの`_convert.py`に置くことを追記
- 2026-11-08: usecaseをドメインごとのディレクトリにし、`core.py`と`_convert.py`に分けることを追記
- 2026-11-08: `_data` の付く関数の決まり（usecase の `_convert.py` で injector を使う関数は `_data` で終え、取るなら `get`、書き込むなら `create`・`save`・`delete`）を追記
- 2026-11-08: 層の表に `domain/aggregate`・`adapter/external` を足し、リンターチェックを `mypy api config`・`ruff` にした
- 2026-11-11: Validation（ドメインのルール）を追記
- 2026-11-12: パッケージ名を `api` から `myus` にした（Django の app の label・テーブル名は変えない）
- 2026-11-12: テストをパッケージの外（`tests/`）に出し、リンターチェックを `mypy myus config tests`・`ruff check myus config tests` にした
- 2026-11-12: adapter を `inbound/`（HTTP・WebSocket）と `outbound/`（外部サービス。もとの `adapter/external`）に分けた
- 2026-11-12: `domain/entity`（Repository の実装）を `adapter/outbound/db` に移した。決済会社の実装は `adapter/outbound/payment`
- 2026-11-12: `domain/interface` をなくし、Data・Interface・ルールを `domain/<ドメイン>/` に置いた
- 2026-11-12: `domain/aggregate` をなくし、集約を `domain/<ドメイン>/<集約>/`（サブスクリプションは `domain/payment/subscription`）に置いた
- 2026-11-12: usecase の入力を DTO にし、schema を `types/schema` から `adapter/inbound/schema` に移した
- 2026-11-12: DTO を `types/dto` から `usecase/dto` に移し、`types` をなくした
- 2026-11-12: import の並び（section の中はパスの名前順、最後に相対パス）と、同じ層の中は相対パスにする決まりを足した
- 2026-11-13: 相対パスの並びを、FE に合わせて近いものから（`.` → `..` → `...`）にした
- 2026-11-13: `utils/functions/index.py` を分けた（`new_ulid` → `utils/functions/id.py`、`create_url` → `utils/functions/url.py`、`get_client_ip` → `adapter/inbound/_common.py`。使われていない `message` は消した）
- 2026-11-12: 中身のわからない `index.py` の名前を変えた（`injectors/module.py`・`domain/media/option.py`・`adapter/outbound/db/base.py`・`adapter/outbound/db/media/query.py`）
