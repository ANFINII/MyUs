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

- **ログ出力形式**: キーワード引数で構造化データを渡す
  ```python
  # Good
  log.info("処理完了", user_id=123, duration=5.2)
  log.error("変換エラー", exc=e, file_path=input_path)

  # Bad
  log.info(f"処理完了: user_id={user_id}")
  ```

### 3. エラーハンドリング
- 例外は適切にキャッチして処理
- エラーログには`exc=e`を渡してスタックトレースを含める
- ユーザーへのエラーメッセージは具体的かつ分かりやすく

### 4. Django規約
- Django固有の書き方は、domain modelとDBモデルの範囲内に限定する
- モデルのフィールドは明示的な型定義
- QuerySetの型ヒントを適切に使用

---

## コーディング規約

### インポート順序
```python
1. 標準ライブラリ
2. サードパーティライブラリ
3. Django関連
4. プロジェクト内モジュール
5. ローカルインポート
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
- 2026-01-21: コーディング規約を大幅に整理・追加（条件判定、早期リターン、リスト内包表記）
- 2026-01-21: 型定義ルールを変更（アダプターはPydantic BaseModel、それ以外はdataclass）
- 2025-10-15: Django Ninjaの型定義ルールを追加
- 2025-09-29: 初版作成
