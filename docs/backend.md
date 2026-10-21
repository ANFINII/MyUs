# バックエンド開発ルール

## 型ヒント

- Python 3.12+の型構文を使用（`list[str]`, `str | None`, `type`文）
- `Callable`は`collections.abc`からインポート
- すべての関数・メソッドに型ヒントを付与

## ロギング

- `print()`禁止、`api.modules.logger`の`log`を使用
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
- **`from X import Y` 文は section 順**: 標準ライブラリ → サードパーティ → Django → プロジェクト内
- **`from x import a, b, c` の中身は domain 順序を維持する**（alphabetical にしない）
  - 例: `from api.db.models.media import Video, Music, Blog, Comic, Picture, Chat` は `MediaType` enum の定義順を保つ
- **`ruff check --fix` を勝手に実行しない**: ruff の isort 挙動は上記ルールと衝突するため、import 整理が必要なときは手動で対応する

## 命名規則

| 対象 | 規則 | 例 |
|------|------|-----|
| 変数・関数 | snake_case | `user_name`, `get_user()` |
| クラス | PascalCase | `VideoConverter` |
| 定数 | UPPER_SNAKE_CASE | `MAX_FILE_SIZE` |
| プライベート | 先頭に`_` | `_internal_method()` |
| Django Model | 単数形 | `User`, `Video` |

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
- Interface・Repository・usecaseは`Result[T, E]`を返す（`from api.utils.common.result import FatalError, NotFoundError, Result`）
- 公開メソッド・usecase関数には`@Result.shield_exception()`を付け、想定外の例外を`FatalError`に変換する
- Resultを受けたらその場で`is_err`を確認し、Errならそのまま返す
- 受け取る変数名: 関数内で受けるResultが1つなら`ret`、複数なら`ids_ret`・`follows_ret`のように`<名前>_ret`
- `injector.get`で取るRepositoryの変数名: その関数のメインのリソースのRepositoryは`repo`、ほかにもRepositoryを使うときは`category_repo`・`user_repo`のように`<名前>_repo`
  - 例: `create_video`は`repo`（動画）と`category_repo`、`upsert_follow`は`repo`（フォロー）と`user_repo`
  - 外部サービス（`PaymentInterface`）も同じ扱い（メインなら`repo`、ほかにメインがあれば`payment_repo`）
- `ok_value`は直接使わず、`ids = ids_ret.ok_value`のように1行で変数に取り出してから使う
- `transaction.atomic()`の中でErrを返すときは、直前に`transaction.set_rollback(True)`を呼ぶ（Errは例外ではないためロールバックされない）

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
- エラー型は`api/utils/common/result/errors.py`の共通型を使う（usecaseごとの`errors.py`は作らない）
- 条件の意味で型を選ぶ（エンドポイントの種類では決めない）
- エラー型に`@final`は付けない

| エラー型 | 使う条件 | `type`（`ErrorType`） | HTTPステータス | message |
|---|---|---|---|---|
| `ValidationError` | 入力や業務ルールに反する（上限超過・ファイル形式等） | `VALIDATION` | 400 | `message` |
| `UnauthorizedError` | 認証されていない | `UNAUTHENTICATED` | 400 | `"Unauthorized"` |
| `ForbiddenError` | 対象はあるが操作する権限がない（持ち主ではない等） | `FORBIDDEN` | 400 | `message` |
| `NotFoundError` | 対象が存在しない（`is None`・`len(ids) == 0`） | `NOT_FOUND` | 400 | `message` |
| `FatalError` | 想定外のエラー（DB・外部APIの例外等） | `INTERNAL` | 500 | `"Internal Server Error"`固定 |

- エラーレスポンスは`ErrorOut`（`type`・`message`）で返す（`api/src/types/schema/common.py`）。`type`は必須
- 成功時に文言だけを返すときは`ErrorOut`ではなく`SuccessOut`（`message`）を使う
- `auth_check`（`api/src/adapter/auth.py`。Cookieからトークンを取り出してusecaseの`verify_token`で確かめる）の結果が`None`（未ログイン）のときも`UNAUTHENTICATED`を返す
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
- サフィックス: 入力`In`、出力`Out`

### 内部データ構造: dataclass
- `@dataclass(frozen=True, slots=True)`
- サフィックス: `Data`
- domain interfaceのdataclassにはフィールドの初期値を設定しない

## アーキテクチャ

### Repository層
- 入出力はdataclass（Django ORMモデルを直接返さない）
- usecase層ではinjector経由でinterfaceを取得（entityを直接インポートしない）

### Interface層（抽象クラス）
- **既存Interfaceの「シグネチャ・命名・構成」に必ず準拠**（独自設計禁止）
- 雛形: `api/src/domain/interface/search_tag/interface.py` を参照
- 必須メソッド: `get_ids(filter, sort, limit)` / `bulk_get(ids)` の読み取り2点
- 任意メソッド（usecaseで必要になったときに追加）: `bulk_save` / `bulk_delete` / `count`
- 必須型: `FilterOption` / `SortOption` dataclass + `SortType` enum
- メソッド追加時は既存パターンと **完全に同じシグネチャ・引数名** を使う（独自シグネチャ禁止）
- 「使わないから書く」「使うから簡略化する」のどちらも禁止：使う分だけ既存の形で書く
- private メソッド（`_` プレフィックス）を Interface に宣言しない（抽象化は公開 API のみ。private ヘルパーは Repository 実装側に置く）
- 雛形と違う形を認めるのは次の場合だけ（新しく足すときも、同じ種類の既存の形に合わせる）
  - `bulk_save`で表せない更新：加算・切り替え・既読など（`save_read`・`save_count`・`save_follow_count`・`media_like`・`comment_like`、通知の`delete`・`delete_by_user`・`confirm`）
  - 一覧に付ける判定：`is_liked`・`get_liked_ids`
  - 認証：`UserInterface.authenticate`
  - メディア・広告の`get_ids(filter, exclude, sort, page, user_id)`：ページング（`PageOption`）とスコア順の`user_id`が要るメディア共通の形
  - カテゴリ・ハッシュタグの`bulk_save(media_type, media_id, objs)`：メディアへの紐づけの保存
  - 外部サービスの窓口（`PaymentInterface`）：DBのリポジトリではないため`get_ids`・`bulk_get`を持たない

### Converterパターン
- `_convert.py`に変換関数を定義
- `convert_data`: Django ORM → dataclass
- `marshal_data`: dataclass → Django ORM

### bulk操作
- `bulk_save`は`get_save_new_ids`（`api/src/domain/entity/index.py`）で保存する
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
| adapter | HTTPリクエスト/レスポンス変換、認証チェック | usecase, schema |
| usecase | ビジネスロジック、複数repositoryの協調 | interface（injector経由） |
| domain/interface | 抽象定義（ABC, dataclass） | なし |
| domain/entity | Repository実装、DBアクセス | Django ORM, interface |

- adapter → usecase → interface の方向にのみ依存する
- usecase層からadapter層の型（`HttpRequest`等）をインポートしない
- usecase層からDjangoのモデル（`User.objects`等）や`authenticate`を直接使わない。リポジトリ（Interface）のメソッドを通す
- domain/interface層は他の層に依存しない（純粋なPython）

## パフォーマンス

- `select_related()`/`prefetch_related()`でN+1回避
- 必要なフィールドのみ`only()`で取得
- QuerySetは遅延評価されるため、評価タイミングを意識する

## テスト

- pytestを使用（Django TestCase不可）
- 今は決済など絶対に失敗できない箇所だけテストを書く（webhook・Stripeの署名の検証・退会時のサブスク解約・outboxの配信）
- `@pytest.mark.django_db`でDB接続
- 実行: `uv run pytest`（`api/tests/`。CIでも実行する）
- テスト用DBは`--nomigrations`でモデルから直接作る（マイグレーションはgit管理外のため）。DBを作る権限のあるユーザーで実行する
- 共通のfixtureは`api/tests/conftest.py`
  - `make_user`: User・Profile・MyPage・UserNotification・UserPlanをまとめて作る
  - `fake_payment`: `PaymentInterface`を`api/tests/fakes.py`の`FakePayment`に差し替える（Stripeを呼ばない。テストごとに元に戻る）

## リンターチェック（必須）

コードを書いた後、必ず実行:

```bash
uv run mypy api/src/path/to/file.py
```

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
