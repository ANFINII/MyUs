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

| エラー型 | 使う条件 | HTTPステータス | message |
|---|---|---|---|
| `ValidationError` | 入力や業務ルールに反する（上限超過・ファイル形式等） | 400 | `error_message` |
| `UnauthorizedError` | 認証されていない | 401 | `"Unauthorized"` |
| `ForbiddenError` | 対象はあるが操作する権限がない（持ち主ではない等） | 403 | `error_message` |
| `NotFoundError` | 対象が存在しない（`is None`・`len(ids) == 0`） | 404 | `error_message` |
| `FatalError` | 想定外のエラー（DB・外部APIの例外等） | 500 | `"Internal Server Error"`固定 |

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
- `case`はHTTPステータスの番号が小さい順に並べ、最後を`case _: assert_never(...)`にする
- BEにしか表示されないメッセージ（500など）は英語にする

```python
ret = update_manage_video(user_id, ulid, input, image)
if ret.is_err:
    match ret.err_value:
        case ValidationError():
            return 400, ErrorOut(message=ret.err_value.error_message)
        case ForbiddenError():
            return 403, ErrorOut(message=ret.err_value.error_message)
        case NotFoundError():
            return 404, ErrorOut(message=ret.err_value.error_message)
        case FatalError():
            return 500, ErrorOut(message="Internal Server Error")
        case _:
            assert_never(ret.err_value)
```

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

### Converterパターン
- `_convert.py`に変換関数を定義
- `convert_data`: Django ORM → dataclass
- `marshal_data`: dataclass → Django ORM

### bulk操作
- `bulk_save`: upsert（`bulk_create(update_conflicts=True)`）
- `get_new_ids`でid未設定オブジェクトに新規ID割り当て

## 層の責務

| 層 | 責務 | 依存してよいもの |
|------|------|------|
| adapter | HTTPリクエスト/レスポンス変換、認証チェック | usecase, schema |
| usecase | ビジネスロジック、複数repositoryの協調 | interface（injector経由） |
| domain/interface | 抽象定義（ABC, dataclass） | なし |
| domain/entity | Repository実装、DBアクセス | Django ORM, interface |

- adapter → usecase → interface の方向にのみ依存する
- usecase層からadapter層の型（`HttpRequest`等）をインポートしない
- domain/interface層は他の層に依存しない（純粋なPython）

## パフォーマンス

- `select_related()`/`prefetch_related()`でN+1回避
- 必要なフィールドのみ`only()`で取得
- QuerySetは遅延評価されるため、評価タイミングを意識する

## テスト

- pytestを使用（Django TestCase不可）
- `@pytest.mark.django_db`でDB接続

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
