# Claude Code バックエンド開発ルール

## 基本原則

### 1. 型ヒント
- **Python 3.9+の新しい型構文を使用**
  - `List[str]` → `list[str]`
  - `Dict[str, int]` → `dict[str, int]`
  - `Optional[str]` → `str | None`
  - `Union[str, int]` → `str | int`
- `collections.abc`から`Callable`をインポート
- 型ヒントは可能な限りすべての関数・メソッドに付与

### 2. ロギング
- **必ず`api.modules.logger`を使用**（`print()`禁止）
  ```python
  from api.modules.logger import log
  ```
- **ログレベルの使い分け**
  | レベル | 用途 |
  |--------|------|
  | `log.debug()` | デバッグ情報 |
  | `log.info()` | 重要な処理の開始・完了 |
  | `log.warning()` | 警告（フォールバック処理など） |
  | `log.error()` | エラー情報（スタックトレース付き） |
  | `log.critical()` | 致命的エラー |

- **ログ出力形式**: 値は必ずキーワード引数で構造化して渡す
  ```python
  # Good - 値をキーワード引数で構造化
  log.info("処理完了", user_id=123, duration=5.2)
  log.error("Channel not found", ulid=ulid)
  log.error("変換エラー", exc=e, file_path=input_path)

  # Bad - f-stringで値を埋め込む
  log.info(f"処理完了: user_id={user_id}")
  log.error(f"Channel not found: {ulid}")
  ```

### 3. エラーハンドリング
- 例外は適切にキャッチして処理
- エラーログには`exc=e`を渡してスタックトレースを含める
- ユーザーへのエラーメッセージは具体的かつ分かりやすく

### 4. Django規約
- Django固有の書き方は、domain modelとDBモデルの範囲内に限定する
- モデルのフィールドは明示的な型定義
- QuerySetの型ヒントを適切に使用

### 5. リンターチェック（必須）
- **Pythonコードを修正したら、必ずmypyでリンターチェックを実行する**
- 修正したファイルに関連するエラーがあれば修正してから完了とする

```bash
# myusディレクトリで実行
uv run mypy api/src/path/to/file.py

# 修正したファイルのエラーのみフィルタする場合
uv run mypy api/src/path/to/file.py 2>&1 | grep "^api/src/path/to/file.py"
```

---

## コーディング規約

### インポート
- **インポートは必ずファイルの先頭で行う**（関数内でのローカルインポート禁止、`TYPE_CHECKING`禁止）
- 型ヒントで使用する型も通常通りインポートする

```python
# Good - ファイル先頭でインポート
from api.db.models.media import Video, Music

def process(obj: Video | Music) -> str:
    return obj.title

# Bad - 関数内でのローカルインポート
def process(obj):
    from api.db.models.media import Video
    ...

# Bad - TYPE_CHECKINGは使用しない
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api.db.models.media import Video
```

**インポート順序:**
```python
1. 標準ライブラリ
2. サードパーティライブラリ
3. Django関連
4. プロジェクト内モジュール
```

### 命名規則
| 対象 | 規則 | 例 |
|------|------|-----|
| 変数・関数 | snake_case | `user_name`, `get_user()` |
| クラス | PascalCase | `VideoConverter` |
| 定数 | UPPER_SNAKE_CASE | `MAX_FILE_SIZE` |
| プライベート | 先頭に`_` | `_internal_method()` |
| Django Model | 単数形 | `User`, `Video` |

### 条件判定

#### リスト/辞書/文字列の空チェック: `len()`を使用
```python
# Good
if len(items) > 0:
    process(items)
if len(items) == 0:
    return []

# Bad
if items:
    process(items)
```

#### Noneの判定: `is None` / `is not None`
```python
# Good
if value is None:
    return default

# Bad
if value == None:
    return default
```

#### ブール値の判定: 直接評価
```python
# Good
if enabled:
    run()

# Bad
if enabled == True:
    run()
```

#### 存在チェック: `in` 演算子
```python
# Good
if key in data:
    value = data[key]

# Bad
if data.get(key) is not None:
    value = data[key]
```

#### 型チェック: `isinstance()`
```python
# Good
if isinstance(obj, str):
    process_string(obj)

# Bad
if type(obj) == str:
    process_string(obj)
```

### リスト内包表記
シンプルな場合のみ使用、複雑ならfor文
```python
# Good - シンプルな変換
names = [user.name for user in users]
active_ids = [u.id for u in users if u.is_active]

# Bad - 複雑すぎる
result = [process(x) for x in items if x.is_valid and x.status == Status.ACTIVE and x.created_at > threshold]

# Good - 複雑な場合はfor文
result = []
for x in items:
    if not x.is_valid:
        continue
    if x.status != Status.ACTIVE:
        continue
    result.append(process(x))
```

### 早期リターン
ガード節でログを出力する
| 状況 | ログレベル |
|------|-----------|
| 正常系 | `log.info` |
| 軽度の異常系 | `log.warning` |
| 危険度が高い | `log.error` |

```python
def process_video(video_id: int) -> Video | None:
    video = Video.objects.filter(id=video_id).first()

    if video is None:
        log.info("動画が見つかりません", video_id=video_id)
        return None

    if video.status == VideoStatus.PROCESSING:
        log.warning("動画は処理中です", video_id=video_id)
        return None

    if video.is_deleted:
        log.error("削除済み動画へのアクセス", video_id=video_id)
        return None

    return video
```

### return文
- **戻り値を変数として利用する場合**: `return None` を明示的に記述
- **ガード節・ループ脱出など変数として利用しない場合**: `return` のみ
- **関数末尾のreturn**: 戻り値を変数として利用しない場合は不要（省略する）

```python
# 戻り値を変数として利用する場合 → return None
def find_user(self, id: int) -> UserData | None:
    if id == 0:
        return None  # 呼び出し元で result = find_user(id) のように使う
    ...

# ガード節で抜ける場合 → return
def bulk_save(self, objs: list[UserData]) -> None:
    if len(objs) == 0:
        return  # 戻り値は使わない、処理を抜けるだけ
    ...
    # 関数末尾のreturnは不要
```

### enum変換
- `match-case`を使用
- 最後に網羅性チェックを追加（`assert_never`推奨、使えない場合は`assert False`）

```python
from enum import Enum
from typing import assert_never

class MediaType(Enum):
    VIDEO = "video"
    MUSIC = "music"
    COMIC = "comic"

def get_media_label(media_type: MediaType) -> str:
    match media_type:
        case MediaType.VIDEO:
            return "動画"
        case MediaType.MUSIC:
            return "音楽"
        case MediaType.COMIC:
            return "漫画"
        case _:
            assert_never(media_type)  # または assert False, f"不正な値: {media_type}"
```

### 非同期処理
- 可能な限り`async/await`を活用
- `asyncio`を使用した並列処理で高速化
- セマフォを使用してリソース制限

```python
import asyncio
from collections.abc import Callable, Awaitable

async def process_parallel(
    items: list[str],
    processor: Callable[[str], Awaitable[dict]]
) -> list[dict]:
    tasks = [processor(item) for item in items]
    return await asyncio.gather(*tasks)
```

---

## 型定義

### アダプター（API）: Pydantic BaseModel
- APIリクエスト/レスポンスのバリデーション用
- サフィックス: 入力に`In`、出力に`Out`

```python
from pydantic import BaseModel

class LoginIn(BaseModel):
    username: str
    password: str

class LoginOut(BaseModel):
    access: str
    refresh: str
```

### 内部データ構造: dataclass
- ドメイン層、ユースケース層などで使用
- サフィックス: `Data`

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class UserData:
    id: int
    username: str
    email: str
```

---

## Repository層

### インターフェースの入出力
- **Repositoryの入出力にはdataclassを使用**（Django ORMモデルを直接返さない）
- 入力: `list[UserData]`などのdataclass
- 出力: `list[UserData]`などのdataclass

```python
# Good - dataclassを使用
class UserInterface(ABC):
    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[UserData]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[UserData]) -> None:
        ...

# Bad - Django ORMモデルを直接返す
class UserInterface(ABC):
    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[User]:  # NG
        ...
```

### Converterパターン
- Repository実装では、dataclass ↔ Django ORMモデル間の変換関数を使用
- `unmarshal`: Django ORMモデル → dataclass（読み取り時）
- `marshal`: dataclass → Django ORMモデル（書き込み時）

```python
# entity/user/data.py

# Unmarshal (Django model -> dataclass)
def user_data(user: User) -> UserData:
    return UserData(
        id=user.id,
        username=user.username,
        ...
    )

# Marshal (dataclass -> Django model)
def marshal_user(data: UserData, user: User) -> None:
    user.username = data.username
    user.email = data.email
    ...
```

### bulk操作
- `bulk_save`: 新規作成・更新を一括で行う（upsert）
- 内部でidの有無を判定して`bulk_create`/`bulk_update`を使い分ける

---

## DBモデル

```python
class Video(models.Model):
    """動画モデル"""
    title: str = models.CharField(max_length=255)
    created_at: datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "動画"
        verbose_name_plural = "動画リスト"
```

---

## パフォーマンス

### データベース
- `select_related()`と`prefetch_related()`でN+1問題を回避
- 必要なフィールドのみ`only()`で取得
- インデックスを適切に設定

### キャッシング
- `@lru_cache`でメソッドの結果をキャッシュ
- Redisを使用したキャッシュ戦略

---

## テスト

**必ずpytestを使用**（Django標準のTestCaseは使わない）

### 基本構成
```python
import pytest
from api.db.models import Video

@pytest.mark.django_db
class TestVideoModel:
    def test_create_video(self):
        video = Video.objects.create(title="Test")
        assert video.title == "Test"
```

### フィクスチャ
```python
# conftest.py
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(
        email="test@example.com",
        username="testuser",
        nickname="Test User",
        password="testpassword"
    )
```

### 実行コマンド
```bash
pytest                      # すべて実行
pytest -v                   # 詳細出力
pytest --cov=api            # カバレッジ付き
pytest -n auto              # 並列実行
pytest -m "not slow"        # slowマーカー以外
```

---

## セキュリティ

- CSRF保護はJWT使用時は不要
- 適切な権限クラスを設定
- シリアライザーで入力を検証
- SQLインジェクション対策（ORMを使用）
- ファイルタイプの検証

---

## プロジェクト固有

### 動画処理
- `VideoConverter`クラスを使用
- ハードウェアアクセラレーションを活用
- 複数解像度の並列生成

### 通知システム
- WebSocketを使用したリアルタイム通知
- `channels`フレームワークを活用

### メディアファイル
- `MEDIA_ROOT`配下に適切に整理
- サムネイル自動生成

### タイムアウト
- フロントエンド: 60秒
- バックエンド: 処理に応じて適切に設定

---

## 運用

### マイグレーション
```bash
python manage.py makemigrations --name descriptive_name
python manage.py showmigrations
python manage.py sqlmigrate app_name 0001
```

### デプロイメント
- `.env`ファイルで環境変数管理
- シークレットキーは絶対にコミットしない
```bash
python manage.py collectstatic --noinput
python manage.py migrate --noinput
```

---

## 更新履歴
- 2026-02-21: return文のルールを追加（明示的return None / ガード節のreturn / 末尾return省略）
- 2026-02-21: bulk_saveの戻り値を`-> None`に統一
- 2026-02-05: bulk操作をbulk_saveに統一（upsertパターン）
- 2026-02-04: Repository層のルールを追加（dataclass入出力、Converterパターン、bulk操作の分離）
- 2026-01-21: コーディング規約を大幅に整理・追加（条件判定、早期リターン、リスト内包表記）
- 2026-01-21: 型定義ルールを変更（アダプターはPydantic BaseModel、それ以外はdataclass）
- 2025-10-15: Django Ninjaの型定義ルールを追加
- 2025-09-29: 初版作成
