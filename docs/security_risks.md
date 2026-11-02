# セキュリティリスク一覧

## 目的

- MyUs のセキュリティリスクを、危険度の順に並べて修正案を示す
- 各項目は `S-01` のような ID で参照する（PR タイトル・本文に ID を書く）
- 直したら「状態」を ✅ にする

凡例: 状態 ⬜ 未着手 / 🚧 対応中 / ✅ 完了

## 一覧（2026-10-26 調査）

| ID | 状態 | 危険度 | 問題 | 場所 |
|---|---|---|---|---|
| S-01 | ✅ | 高 | 管理画面のログインに回数の制限が無い。`/myus-manage/` は一般のユーザーもログインできる | `config/urls.py`、`api/admin.py:374-386` |
| S-02 | ✅ | 高（要確認） | アップロードされた動画・音声を、形式を確かめずに ffmpeg / ffprobe に渡している | `api/utils/functions/media.py`、`api/utils/functions/convert/video_converter.py:260, 295`、`audio_converter.py:27-35` |
| S-03 | ✅ | 中 | ログイン・メール送信の回数の制限がプロセスごとのメモリに記録され、プロセスの数だけ緩くなる | `config/settings/base.py`（`CACHES` が無い）、`api/src/adapter/auth.py:13-18` |
| S-04 | ✅ | 中 | ログアウトしてもトークンが失効しない（refresh トークンは 30 日有効） | `api/src/adapter/auth.py:172-178`、`api/utils/functions/token.py` |
| S-05 | ✅ | 中 | ログインの回数の制限が IP 単位だけで、アカウント単位の上限が無い | `api/src/adapter/auth.py:142` |
| S-06 | ✅ | 低 | 画像の中身（マジックバイト）を確かめず、拡張子と申告の `content_type` だけで受け付けている | `api/utils/functions/media.py` |
| S-07 | ✅ | 中 | パスワードの確認で Django の `validate_password` を呼んでおらず、よくあるパスワードを登録できる。登録・変更・リセットで確認の内容も違う | `api/src/usecase/user.py:310`、`api/src/usecase/auth.py:267, 394`、`api/utils/functions/validation.py:6-7` |

---

## S-01 管理画面のログインに回数の制限が無い

### 問題

- `config/urls.py` は、Django admin を 2 つ公開している

  ```python
  path("myus-admin/", admin.site.urls),
  path("myus-manage/", manage_site.urls),
  ```

- API の `/login` には `LoginThrottle("10/m")` があるが、Django admin のログイン画面はこの制限を通らない。ここからならパスワードを何回でも試せる
- `/myus-manage/`（`MyUsAdminSite`）は、`has_permission` が `is_active` しか見ていない。管理者でない一般のユーザーもログインできる

  ```python
  def has_permission(self, request):
      return request.user.is_active
  ```

- `/myus-manage/` は旧実装の投稿管理の画面で、新実装（`frontend/` の `/manage/*`）の API を通らない。そのため、API に入れたアップロードの検証（`validate_uploads`）などが効かない
- `/myus-admin/` を破られると、DB のすべてのデータを操作される

### 修正案

1. `/myus-manage/` を使っていなければ外す（新実装の `/manage/*` に置き換わっているため）
   - `config/urls.py` から `path("myus-manage/", manage_site.urls)` を消す
   - `api/admin.py` の `MyUsAdminSite` と、`manage_site.register(...)` をすべて消す
2. `/myus-admin/` を守る。次のうち、できるものから入れる
   - nginx で、管理画面のパスを自分の IP にだけ許可する（一番効く）

     ```nginx
     location /myus-admin/ {
         allow <自分の IP>;
         deny all;
         proxy_pass http://myus_backend;
     }
     ```

   - パスを環境変数にし、推測しにくい値にする（`path(f"{env.admin_path}/", admin.site.urls)`）
   - ログインの回数の制限を入れる（`django-axes` など。S-03 の共有キャッシュと合わせる）
   - スタッフのアカウントは、ほかでは使わない長いパスワードにする

---

## S-02 アップロードされた動画・音声を、形式を確かめずに ffmpeg に渡している（要確認）

### 問題

- アップロードの検証（`validate_uploads`）は、拡張子とブラウザが申告する `content_type` だけを見ている。どちらも送る側が自由に決められる
- ffmpeg / ffprobe は、拡張子ではなく中身から形式を判定する。そして入力の形式もプロトコルも制限せずに `-i` で読んでいる

  ```python
  cmd = [self.ffmpeg_path, ..., '-i', input_path, ...]
  ```

- そのため、次の攻撃が通る可能性がある
  1. HLS のプレイリスト（テキスト）を作り、サーバー上のファイル（例: `file:///code/envs/django.env`）を読み込む指示を書く
  2. それを `video.mp4` と名付け、`content_type: video/mp4` で上げる
  3. ffmpeg はプレイリストとして読み、指定したファイルを取り込んで動画にする
  4. 変換後の動画を再生すると、ファイルの中身が見える
- 通るかどうかは ffmpeg のバージョンと設定による。手元では試していない

### 修正案

1. 変換する前に ffprobe で形式を調べ、許可した形式のときだけ変換する。ffprobe 自体も、ファイルの読み込みだけに制限して呼ぶ

   ```python
   ALLOWED_VIDEO_FORMATS = {"mov", "mp4", "m4a", "3gp", "3g2", "mj2", "matroska", "webm", "avi"}
   ALLOWED_AUDIO_FORMATS = {"mp3", "wav", "flac", "ogg", "mov", "mp4", "m4a", "aac", "asf", "aiff"}


   def probe_format(path: str) -> Result[set[str], ValidationError]:
       cmd = ["ffprobe", "-v", "error", "-protocol_whitelist", "file", "-show_entries", "format=format_name", "-of", "json", path]
       result = subprocess.run(cmd, capture_output=True, text=True, timeout=PROBE_TIMEOUT)
       if result.returncode != 0:
           log.warning("ffprobe failed", path=path)
           return Result.err(ValidationError("error.fileTypeInvalid"))

       format_name = json.loads(result.stdout)["format"]["format_name"]
       return Result.ok(set(format_name.split(",")))
   ```

   - `format_name` は `mov,mp4,m4a,3gp,3g2,mj2` のようにカンマ区切りで返る。分けた集合が許可の集合に含まれるときだけ通す
   - `hls`・`concat`・`ffconcat`・`image2` などのプレイリストや連番の形式は、許可の集合に入れない
2. ffmpeg の呼び出しにも `-protocol_whitelist file` を付け、ファイル以外のプロトコル（http・tcp など）を読ませない
3. ffmpeg に `-f` で入力の形式を明示する（1. で調べた形式を渡す）
4. 1〜3 を、`create_video`・`create_music` から変換を呼ぶ前に通す。失敗したら `ValidationError("error.fileTypeInvalid")` を返し、保存したファイルを消す
5. 余裕があれば、変換を別のコンテナで動かし、そのコンテナには `envs/` や DB の接続情報を置かない

---

## S-03 回数の制限がプロセスごとのメモリに記録される

### 問題

- django-ninja の throttling は、Django の既定のキャッシュ（`django.core.cache.cache`）に回数を記録する
- `config/settings/` に `CACHES` の設定が無いため、既定の `LocMemCache`（プロセスごとのメモリ）が使われる
- そのため次のことが起きる
  - プロセスが複数あると、制限の回数がプロセスの数だけ増える（4 プロセスなら `10/m` が実質 `40/m`）
  - 再起動するたびに、回数が消える

### 修正案

Redis は Channels のために既にあるので、キャッシュも Redis に置く。

```python
# config/settings/base.py
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{env.redis_host}:{env.redis_port}/1",
    }
}
```

- Channels の `CHANNEL_LAYERS` と同じ Redis を使い、DB の番号だけ分ける（Channels は 0、キャッシュは 1）
- Redis にパスワード（`REDIS_PASSWORD`）を設定しているので、`config/env.py` に `redis_password` を足し、URL に入れる（`redis://:<password>@host:port/1`）

---

## S-04 ログアウトしてもトークンが失効しない

### 問題

- ログアウトは Cookie を消すだけで、トークン自体は有効なまま

  ```python
  def logout(request: HttpRequest, response: HttpResponse):
      response.delete_cookie("access_token")
      response.delete_cookie("refresh_token")
      return 200, None
  ```

- refresh トークンは 30 日有効。Cookie を盗まれると、パスワードを変えるまで使われ続ける
- パスワードを変えたときに古いトークンが無効になる仕組み（`pwd` の指紋）はある

### 修正案

最小の対応は、ユーザーにトークンの版を持たせ、ログアウトで版を上げること。

1. `User` に `token_version = models.PositiveIntegerField(default=0)` を足す
2. `access_token`・`refresh_token` の payload に `"ver": token_version` を入れる
3. `verify_token` で、payload の `ver` と DB の `token_version` が同じか確かめる（今の `is_same_password` の確認の隣）
4. `/logout` で、ログイン中のユーザーの `token_version` を `F("token_version") + 1` で上げる。退会のときも上げる

この方法では、ログアウトするとほかの端末もまとめてログアウトする。端末ごとにログアウトさせたいときは、セッションをサーバー側に持つ形にする。

---

## S-05 ログインの回数の制限が IP 単位だけ

### 問題

- `LoginThrottle` は `AnonRateThrottle` で、IP ごとに `10/m` の制限をかけている
- IP を変えながら 1 つのアカウントを狙う総当たりは止まらない
- `10/m` は 1 日で 14,400 回になり、弱いパスワードなら破られる

### 修正案

アカウント（`username`）単位の上限を足す。判定は domain の純粋な関数にし、試行の時刻は Redis に記録する。

1. 判定の関数を置く

   ```python
   @dataclass(frozen=True, slots=True)
   class AttemptLimitData:
       max_attempts: int
       window: timedelta


   LOGIN_LIMITS = (AttemptLimitData(max_attempts=10, window=timedelta(minutes=15)), AttemptLimitData(max_attempts=50, window=timedelta(hours=24)))


   def is_blocked(limits: tuple[AttemptLimitData, ...], attempted_at: list[datetime], now: datetime) -> bool:
       for limit in limits:
           count = len([t for t in attempted_at if now - t < limit.window])
           if count >= limit.max_attempts:
               return True
       return False
   ```

2. `login_user` で、パスワードを確かめる前に判定する。超えていたら `ValidationError("error.tooManyAttempts")` を返す
3. ログインに失敗したら、その時刻を Redis の sorted set（キー: `login_attempt:<username>`）に足す。成功したら消す
4. FE の `common.json`（ja / en）の `error` に `tooManyAttempts` を足す
5. 存在しない `username` でも同じく記録し、アカウントがあるかを応答の違いで分からないようにする

---

## S-06 画像の中身を確かめていない

### 問題

- 画像は、拡張子と申告の `content_type` だけで受け付けている
- SVG は許可していないため、画像として HTML やスクリプトが動く危険は小さい
- ただし、画像ではないファイル（HTML など）を `.jpg` として置けてしまう

### 修正案

1. Pillow（既に依存にある）で開いて、許可した形式か確かめる

   ```python
   with Image.open(file) as image:
       image.verify()
       if image.format not in {"JPEG", "PNG", "GIF", "WEBP"}:
           return Result.err(ValidationError("error.fileTypeInvalid"))
   file.seek(0)
   ```

2. メディアを配信する nginx で `X-Content-Type-Options: nosniff` を付け、ブラウザに中身から形式を推測させない

---

## S-07 パスワードの強さを Django の検証で確かめていない

### 問題

- パスワードは PBKDF2-SHA256（150 万回、ユーザーごとのソルト付き）で保存しており、レインボーテーブルには強い。ただし、よくあるパスワードは辞書攻撃ですぐに破られる
- `config/settings/base.py` の `AUTH_PASSWORD_VALIDATORS` には `CommonPasswordValidator` などがあるが、API から `validate_password` を呼んでいないため効いていない。`password1` のようなよくあるパスワードを登録できる
- 確認の内容が、登録・変更・リセットで揃っていない

| 処理 | 場所 | 確かめていること |
|---|---|---|
| 新規登録 | `api/src/usecase/user.py:310`（`signup_check`） | 8 文字以上、英字と数字を含む（上限なし） |
| パスワードの変更 | `api/src/usecase/auth.py:267`（`change_password`） | 8〜16 文字（英字・数字は見ない） |
| パスワードのリセット | `api/src/usecase/auth.py:394`（`reset_password`） | 8〜16 文字（英字・数字は見ない） |

- 変更・リセットの上限が 16 文字（`PASSWORD_MAX_LENGTH`）のため、長いパスフレーズを使えない

### 修正案

1. パスワードの確認を 1 つの関数にまとめ、登録・変更・リセットの 3 箇所から呼ぶ

   ```python
   # api/utils/functions/validation.py
   PASSWORD_MIN_LENGTH = 8
   PASSWORD_MAX_LENGTH = 128


   def password_error(password: str, user: User | None) -> str | None:
       if len(password) < PASSWORD_MIN_LENGTH or len(password) > PASSWORD_MAX_LENGTH:
           return "error.passwordInvalid"

       if not has_number(password) or not has_alphabet(password):
           return "error.passwordInvalid"

       try:
           validate_password(password, user)
       except DjangoValidationError:
           return "error.passwordTooCommon"

       return None
   ```

   - `validate_password` に `user` を渡すと、`UserAttributeSimilarityValidator` がユーザー名・メールアドレスに似たパスワードも弾く。新規登録では、まだ保存していない `User(email=..., username=..., nickname=...)` を作って渡す
   - usecase から Django の関数を直接呼ばない規約（`docs/backend.md` の「層の責務」）に合わせるなら、`validate_password` の呼び出しは domain/entity 側の関数に置く
2. `PASSWORD_MAX_LENGTH` を 128 に上げる（PBKDF2 は長さで計算時間がほぼ変わらない。極端に長い入力による負荷だけを防ぐ）
3. FE の `frontend/src/lib/i18n/locales/{ja,en}/common.json` の `error` に `passwordTooCommon` を足す。`passwordInvalid` の文言は、上限を変えたら合わせて直す
4. 既に登録済みの弱いパスワードは、次のログインのときに変更を促すかを別に決める（今回の修正の対象外にしてよい）
