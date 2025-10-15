# Claude Code バックエンド開発ルール

## 基本原則

### 1. Python型ヒント
- **Python 3.9+の新しい型構文を使用**
  - `List[str]` → `list[str]`
  - `Dict[str, int]` → `dict[str, int]`
  - `Optional[str]` → `str | None`
  - `Union[str, int]` → `str | int`
- `collections.abc`から`Callable`をインポート
- 型ヒントは可能な限りすべての関数・メソッドに付与

### 2. ロギング
- **必ず`api.modules.logger`を使用**
  - `from api.modules.logger import log`
  - `print()`文は使用禁止
- ログレベルの使い分け
  - `log.debug()`: デバッグ情報
  - `log.info()`: 重要な処理の開始・完了
  - `log.warning()`: 警告（フォールバック処理など）
  - `log.error()`: エラー情報（スタックトレース付き）
  - `log.critical()`: 致命的エラー
- **ログ出力形式**
  - キーワード引数で構造化データを渡す
  - `log.info("処理完了", user_id=123, duration=5.2)`
  - `log.error("エラー発生", exc=e, path=file_path)`
  - f-stringは簡単なメッセージのみに使用

### 3. エラーハンドリング
- 例外は適切にキャッチして処理
- エラーログには`exc=e`を渡してスタックトレースを含める
- ユーザーへのエラーメッセージは具体的かつ分かりやすく

### 4. Django規約
- モデルのフィールドは明示的な型定義
- QuerySetの型ヒントを適切に使用
- ビューは`APIView`または`ViewSet`を継承

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
- **変数・関数**: snake_case
- **クラス**: PascalCase
- **定数**: UPPER_SNAKE_CASE
- **プライベート**: 先頭に`_`
- **Django Model**: 単数形（例: `User`, `Video`）

### 非同期処理
- 可能な限り`async/await`を活用
- `asyncio`を使用した並列処理で高速化
- セマフォを使用してリソース制限

## Django固有ルール

### 型定義（Django Ninja）
- **入力（Input）データ型**: `ninja.Schema` を使用
  - APIリクエストボディのバリデーション用
  - `from ninja import Schema` でインポート
  - 例: `SignUpDataIn`, `LoginDataIn`, `VideoDataIn`

- **出力（Output）データ型**: `@dataclass` を使用
  - APIレスポンス用のデータクラス
  - `from dataclasses import dataclass` でインポート
  - `@dataclass(frozen=True, slots=True)` を推奨
  - 例: `LoginOutData`, `VideoData`, `ErrorData`

```python
# 入力用（ninja.Schema）
from ninja import Schema

class LoginDataIn(Schema):
    username: str
    password: str

# 出力用（dataclass）
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class LoginOutData:
    access: str
    refresh: str
    user: UserLoginData

@dataclass(frozen=True, slots=True)
class ErrorData:
    message: str
```

### モデル
```python
class Video(models.Model):
    """動画モデル"""
    title: str = models.CharField(max_length=255)
    created_at: datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "動画"
        verbose_name_plural = "動画リスト"
```

### ビュー
```python
from rest_framework.views import APIView
from api.modules.logger import log

class VideoAPI(APIView):
    def post(self, request) -> Response:
        log.info("VideoAPI POST - リクエスト開始")
        try:
            # 処理
            return Response(data, status=HTTP_201_CREATED)
        except Exception as e:
            log.error("エラー発生", exc=e)
            return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
```

### タイムアウト設定
- フロントエンド: 60秒（1分）
- バックエンド: 処理に応じて適切に設定

## パフォーマンス最適化

### データベース
- `select_related()`と`prefetch_related()`でN+1問題を回避
- 必要なフィールドのみ`only()`で取得
- インデックスを適切に設定

### キャッシング
- `@lru_cache`でメソッドの結果をキャッシュ
- Redisを使用したキャッシュ戦略

### 並列処理
```python
import asyncio
from collections.abc import Callable

async def process_parallel(
    items: list[str],
    processor: Callable[[str], Awaitable[dict]]
) -> list[dict]:
    """並列処理の例"""
    tasks = [processor(item) for item in items]
    return await asyncio.gather(*tasks)
```

## セキュリティ

### 認証・認可
- JWT認証を使用（`rest_framework_simplejwt`）
- CSRF保護はJWT使用時は不要
- 適切な権限クラスを設定

### 入力検証
- シリアライザーで入力を検証
- SQLインジェクション対策（ORMを使用）
- ファイルタイプの検証

## テスト

### テストフレームワーク
**必ずpytestを使用**
- Django標準のTestCaseではなく、pytestを使用
- `pytest-django`プラグインを利用
- フィクスチャベースのテスト設計

### pytest設定
```python
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.base
python_files = tests.py test_*.py *_tests.py
python_classes = Test*
python_functions = test_*
testpaths = api/tests
addopts = -v --tb=short --strict-markers --reuse-db
```

### ユニットテスト
```python
import pytest
from api.modules.logger import log
from api.models import Video

@pytest.mark.django_db
class TestVideoModel:
    def setup_method(self):
        log.info("テストセットアップ")

    def test_create_video(self):
        """動画作成テスト"""
        # テスト実装
        video = Video.objects.create(title="Test")
        assert video.title == "Test"
```

### フィクスチャの活用
```python
# conftest.py
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user():
    """テストユーザーを作成"""
    return User.objects.create_user(
        email="test@example.com",
        username="testuser",
        nickname="Test User",
        password="testpassword"
    )

@pytest.fixture
def authenticated_client(client, user):
    """認証済みクライアントを作成"""
    client.login(username="testuser", password="testpassword")
    return client
```

### テスト実行コマンド
```bash
# すべてのテストを実行
pytest

# 特定のファイルを実行
pytest api/tests/test_login.py

# 詳細な出力付き
pytest -v

# カバレッジレポート付き
pytest --cov=api

# 新しいデータベースで実行
pytest --create-db

# 並列実行（高速化）
pytest -n auto
```

### マーカーの使用
```python
@pytest.mark.slow
def test_heavy_processing():
    """時間のかかるテスト"""
    pass

@pytest.mark.unit
def test_simple_function():
    """ユニットテスト"""
    pass

# 実行時にマーカーで絞り込み
# pytest -m "not slow"  # slowマーカー以外を実行
# pytest -m unit        # unitマーカーのみ実行
```

### 統合テスト
- APIエンドポイントのテスト
- 認証フローのテスト
- ファイルアップロードのテスト
- WebSocketのテスト

## デバッグ

### ログ活用
```python
# 構造化ログの推奨形式
log.info("MP4パス設定成功", mp4_path=mp4_path)
log.warning("フォールバック処理", original_path=original, fallback_path=fallback)
log.error("変換エラー", exc=e, file_path=input_path, resolution="720p")

# 処理の追跡
log.info("処理開始", process="video_encoding")
# ... 処理 ...
log.info("処理完了", process="video_encoding", duration=time.time() - start)

# 悪い例（f-stringで全て結合）
log.info(f"MP4パス設定成功: {mp4_path}")  # ✗ 構造化されていない

# 良い例（キーワード引数で構造化）
log.info("MP4パス設定成功", mp4_path=mp4_path)  # ✓ 構造化されている
```

## プロジェクト固有ルール

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
- CDN対応を考慮した設計

## マイグレーション

### 作成時の注意
```bash
python manage.py makemigrations --name descriptive_name
```

### 実行前確認
```bash
python manage.py showmigrations
python manage.py sqlmigrate app_name 0001
```

## デプロイメント

### 環境変数
- `.env`ファイルで管理
- 本番環境では環境変数から読み込み
- シークレットキーは絶対にコミットしない

### 静的ファイル
```bash
python manage.py collectstatic --noinput
```

### データベース
```bash
python manage.py migrate --noinput
```

## 更新履歴
- 2025-10-15: Django Ninjaの型定義ルールを追加（Schema vs dataclass）
- 2025-09-29: 初版作成（バックエンド開発ルール）
