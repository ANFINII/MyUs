# 旧実装（Django テンプレート）移行ロードマップ

## 目的

- 旧実装（`myus/templates/` + `myus/app/`）にあり、新実装（`frontend/` + `myus/api/`）にまだ無い機能を移行する
- 移行が終わったら旧実装（`app.urls` のルーティング・テンプレート）を撤去できる状態にする

## 進め方の原則

- 1 フェーズ内でも **BE → FE の順に、独立してマージ可能な PR** に切る
- BE は Result 型の規約（`Result[T, FatalError]`・`xxx_ret` / `ret`・`ok_value` は変数に取り出す・500 は `Internal Server Error`）に従う
- 仕様を決める必要があるもの（「決めること」）は、着手前に決めてからPRにする
- mypy（`uv run mypy`）・`npm run lint` を pass させる

---

## 現状（2026-10-19 調査）

旧実装の機能のうち、新実装に無い・一部だけあるもの。

| # | 旧実装の機能 | 状況 | 旧実装 | 新実装 |
|---|---|---|---|---|
| 1 | メディア詳細の広告表示（全体広告 1 件 ＋ 投稿者の個別広告をプランに応じて 1〜4 件） | 完了（#989・#1140） | `app/modules/context_data.py:94-104`、`templates/parts/common/common.html:84-95` | `frontend/src/components/widgets/Advertise/index.tsx` は空の枠だけ。`isAd` を渡している所がなく表示されない |
| 2 | 広告のクリック数カウント | API のみ | `url/read` → `advertise_read` | `POST /advertise/{ulid}/read` はあるが、FE の `postAdvertiseRead` は未使用 |
| 3 | 全体広告（`type="all"`） | 完了（#1140） | `Advertise.objects.filter(publish=True, type=0).order_by("?")[:1]` | 取得する API も FE も無い |
| 4 | 広告の自動再生設定（`is_advertise`） | 対象外（`is_advertise` は全体広告の表示設定にした。D2） | `advertise_article_auto.html` | 設定画面で保存はできるが、広告を出していないので効いていない |
| 5 | ユーザーページの「広告」タブ（検索付き） | 未移行 | `userpage/advertise/<nickname>` | `components/templates/userpage/index.tsx` は「情報」「投稿」の 2 タブのみ |
| 6 | ユーザーページの投稿内検索 | 未移行 | `userpage/post?search=`（`Search.search_userpage`） | `GET /user/userpage/{ulid}/media` は `channel_ulid` のみ受け取る |
| 7 | Google Tag Manager（サイト全体 `GTM-5F3M5PR` ＋ 投稿者ごとの `tag_manager_id`） | 未移行 | `templates/base.html`、`templates/parts/google_tag_user.html` | FE に読み込みが無い。マイページで ID は登録できるが未使用 |
| 8 | 音楽ダウンロードを Premium / Ultimate の閲覧者に限定 | 一部 | `templates/media/music/music_detail.html:21` | `templates/media/music/detail.tsx` は `download` フラグのみ確認。API にもプラン確認が無い |
| 9 | 動画の音量を覚えておく | 未移行（小） | `static/js/video_volume.js`（cookie） | `widgets/Video`・`AudioPlayer` に保存処理なし |
| 10 | 決済キャンセル時の画面 | 一部（小） | `setting/payment/cancel` | Stripe の cancel_url が `/setting/payment` に戻るだけでメッセージなし（`adapter/payment.py`） |

### 移行対象外（作り直し済み）

- 詳細画面のフォロー → チャンネル購読（`SubscribeButton`）。ユーザーのフォローはユーザーページから
- 退会の 2 段階認証（パスワード → 60 秒トークン → パスワード）→ パスワード確認 1 回
- 急上昇（おすすめ）の計算式の変更
- 投稿を公開側 `/media/*/create` から管理画面 `/manage/*/create` に移動
- pjax（SPA なので不要）、`promotion.js`（どこからも読み込まれていない）、`app/ai/analytics.py`（単体スクリプト）

---

## 決めること（着手前）

| # | 内容 | 関連フェーズ |
|---|---|---|
| D1 | 全体広告を誰に出すか。料金プランの説明（`api/utils/plan.py`）では有料プランは「全体広告OFF」。閲覧者のプランで出し分けるか、旧実装どおり常に出すか | Phase 1 |
|  | → 決定：閲覧者で出し分ける。全体広告はすべての詳細に出し、無料プラン・未ログインの閲覧者には常に出す。有料プランの閲覧者は、マイページの設定（`is_advertise`）でオフにできる。個別広告はオフにしても表示する | |
| D2 | 全体広告の自動再生（`is_advertise`）は閲覧者の設定か、投稿者の設定か（旧実装は閲覧者のマイページ設定） | Phase 1 |
|  | → 決定：`is_advertise` は自動再生ではなく、閲覧者の全体広告の表示設定（マイページの「全体広告」。有料プランだけ変更できる）とする | |
| D3 | ユーザーページの投稿内検索は、チャンネル絞り込みと併用するか置き換えるか | Phase 2 |
| D4 | GTM は今も使うか（サイト全体の `GTM-5F3M5PR` が有効か）。投稿者の `tag_manager_id` を他人のページに埋め込む機能を続けるか | Phase 3 |
| D5 | 音楽ダウンロードの制限は「閲覧者のプラン」で良いか（旧実装は閲覧者のプランで判定） | Phase 4 |

---

## Phase 1: 広告の表示（#1〜#4）

最も大きい未移行部分。BE の個別広告取得（`GET /advertise/user/{user_ulid}`）とクリック数（`POST /advertise/{ulid}/read`）は既にある。

### PR 1-1【back】全体広告を取得する API を追加する

- `usecase/advertise.py` に全体広告（`type="all"`・公開中・期間内）をランダムに 1 件返す関数を追加
- `adapter/advertise.py` に `GET /advertise/global`（仮）を追加
- D1 で閲覧者のプランで出し分ける場合は、ここで閲覧者のプランを見て空を返す
- 完了条件：mypy pass、全体広告が無い・期間外のときは空リスト

### PR 1-2【front】メディア詳細に広告を表示する

- `widgets/Advertise/index.tsx` の空の枠を実装（画像 / 動画・タイトル・リンク）
- 詳細画面（`widgets/Media/Detail/Common.tsx` → `Right.tsx`）に `isAd` / `isChannelAd` を渡す
- 投稿者の ulid で `getUserAdvertises` を呼んで個別広告を、PR 1-1 の API で全体広告を取得
  - 取得は useEffect ではなく、詳細の取得と同じ流れ（loader / useQuery）で行う
- 完了条件：プランに応じた件数の個別広告と全体広告が表示される、`npm run lint` pass

### PR 1-3【front】広告クリックで閲覧数を数える

- 広告のリンクを押したときに `postAdvertiseRead` を呼んでから遷移する
- 完了条件：クリックで `read` が増える（管理画面の広告一覧で確認）

### PR 1-4【front】広告の自動再生設定を反映する

- D2 の結果に沿って、`isAdvertise` が true のとき広告の動画を自動再生する
- 完了条件：設定の ON / OFF で自動再生が切り替わる

---

## Phase 2: ユーザーページ（#5・#6）

### PR 2-1【back】ユーザーの広告一覧 API に検索を追加する

- ユーザーページ用に、そのユーザーの公開広告を検索語で絞り込んで返す（既存 `get_user_advertises` はランダム抽出なので別関数にする）
- 完了条件：mypy pass

### PR 2-2【front】ユーザーページに「広告」タブを追加する

- `components/templates/userpage/index.tsx` に 3 つ目のタブを追加し、検索入力付きで一覧を表示
- 完了条件：`npm run lint` pass

### PR 2-3【back】ユーザーページの投稿取得に検索語を追加する

- `GET /user/userpage/{ulid}/media` に `search` を追加し、`get_userpage_media` に渡す（`get_videos` などは既に `search` を受け取れる）
- D3 の結果に沿って `channel_ulid` と併用する
- 完了条件：mypy pass

### PR 2-4【front】ユーザーページの投稿タブに検索を追加する

- 投稿タブに検索入力を追加し、PR 2-3 の `search` を渡す
- 完了条件：検索語で投稿が絞り込まれる

---

## Phase 3: Google Tag Manager（#7）

D4 で「使う」と決まった場合のみ。

### PR 3-1【front】サイト全体の GTM を読み込む

- `frontend/index.html` か起動時の処理で GTM を読み込む（ID は環境変数にする）
- 完了条件：本番ビルドでのみ読み込まれる

### PR 3-2【back】【front】投稿者の GTM をメディア詳細で読み込む

- BE：メディア詳細のレスポンス（`MediaUserOut` など）に投稿者の `tag_manager_id` を含める
- FE：詳細画面で投稿者の `tag_manager_id` があれば GTM を読み込み、画面を離れたら外す
- 完了条件：`tag_manager_id` を設定した投稿者のページでだけ読み込まれる

---

## Phase 4: 音楽ダウンロードのプラン制限（#8）

### PR 4-1【back】音楽詳細でダウンロード可否を返す

- `get_music_detail` で閲覧者のプラン（D5）を見て、ダウンロードできるかを `MusicDetailOut` に含める（例：`can_download`）
- ダウンロード用 URL を返す API がある場合は、そこでもプランを確認する
- 完了条件：Free / Basic / Standard の閲覧者は false、Premium / Ultimate は `download` フラグに従う

### PR 4-2【front】ダウンロードボタンをプランで出し分ける

- `templates/media/music/detail.tsx` で `download` ではなく PR 4-1 の値でボタンを出す
- 完了条件：`npm run lint` pass

---

## Phase 5: 小さいもの（#9・#10）

### PR 5-1【front】動画・音楽の音量を保存する

- `widgets/Video`・`AudioPlayer` で音量を localStorage に保存し、次回の再生時に戻す（try/catch で囲む）

### PR 5-2【back】【front】決済キャンセル時にメッセージを出す

- BE：Stripe の cancel_url を `/setting/payment/cancel` にする（`adapter/payment.py`）
- FE：決済完了画面（`/setting/payment/success`）と対になる決済キャンセル画面を追加する（旧実装の `setting/payment/cancel` と同じ構成。クエリを見てトーストを出す案は、表示時に useEffect が必要になるため採らない）

---

## Phase 6: 旧実装の撤去

### 削除の障壁（新実装が旧実装に依存している箇所）

旧実装を消すと新実装まで壊れる箇所。削除より先に api 側へ移す。

| # | 障壁 | 消すと壊れるもの | 対応 |
|---|---|---|---|
| B1 | `config/asgi.py` が `app/routing.py` → `app/consumers.py`（`ChatConsumer`）を読み込んでいる | チャットの WebSocket（新 FE の `useChatWebSocket` と `usecase/broadcast.py`） | `api/src/adapter/websocket.py` に移動（完了） |
| B2 | `api/src/usecase/auth.py` が `templates/registration/email/` を `render_to_string` で読んでいる | 会員登録・パスワード再設定のメール送信 | `api/templates/registration/email/` に移動し、`TEMPLATES["DIRS"]` に追加（完了） |
| B3 | `templates/admin/base_site.html` が管理画面の見た目を上書きしている | `/myus-admin/` の見た目（`static/css/admin.css`・`base_site.css` を読み込む） | `api/templates/admin/` に移動（完了） |

B1〜B3 は PR 6-1 で対応済み（ブランチ `back_fix_legacy_removal_blockers`）。

### PR 6-1【back】旧実装の削除に備え、WebSocket とテンプレートを api 側に移す（完了）

- `ChatConsumer` と `websocket_urlpatterns` を `api/src/adapter/websocket.py` に移し、`config/asgi.py` の参照先を変更
  - asgi の起動時に読み込まれるため、モデルを import しないモジュールに置く
  - `channels` の `WebsocketConsumer` は型情報が無いため、`pyproject.toml` でこのモジュールだけ `disallow_subclassing_any` / `disallow_any_unimported` を外す
- メールテンプレートと管理画面の `base_site.html` を `api/templates/` に `git mv`
- `TEMPLATES["DIRS"]` を `[api/templates, templates]` にする（旧実装もメールテンプレートを使うため、削除までは `templates` も残す）
- 確認：mypy で新しいエラーなし、`manage.py check` pass、テンプレートが `api/templates` から読まれる、WebSocket に接続して group_send したメッセージを受信できる

### PR 6-2【back】旧実装のルーティングとテンプレートを削除する（完了）

当初は Phase 1〜5 の後に行う予定だったが、利用者が使うのは Vercel の FE で、旧実装の画面はバックエンドのドメインに直接アクセスしたときにしか見えないため、先に削除した。未移行の機能は元々新実装に無いので、削除しても使える機能は減らない（Phase 1〜5 は引き続き新実装で対応する）。

- 旧実装専用だった `api/utils/` のモジュール・関数・定数も削除（`decorators/auth.py`・`enum/response.py`・`filter_data.py`・`functions/search.py`・`functions/convert/convert_hls.py`・`functions/convert/master_m3u8.py`、`is_bool`・`set_attr`・`email_user`・`notification_type_no`・`model_list` など）

- `config/urls.py` から `path("", include("app.urls"))` と `path("setting/", include("django.contrib.auth.urls"))` を外す
- `config/settings/base.py` から `LOGIN_URL = "app:login"`・`LOGIN_REDIRECT_URL = "app:index"`・`LOGOUT_REDIRECT_URL = "app:login"` を外し、`TEMPLATES["DIRS"]` を `api/templates` だけにする
- `myus/app/`・`myus/templates/` を削除（`templates/admin/myusapp/` は api アプリのラベルが `db` のため元から使われていない）
- `myus/static/` は次だけ残して削除
  - `img/user_icon.png`・`img/MyUs_banner.png`（`api/db/models/user.py`・`channel.py` の初期画像）
  - `css/admin.css`・`css/base_site.css`（管理画面）
- `api/utils/` などで旧実装からしか使われていない関数も削除
- 404 / 500 / 403 のテンプレートは旧実装の `base2.html` を継承しているので一緒に消す（Django 標準の画面になる。API は JSON を返すので影響なし）
- 完了条件：mypy pass、`manage.py check` pass、FE の全画面とチャットの WebSocket・メール送信・管理画面が動く

---

## 進捗

| フェーズ | 状況 |
|---|---|
| 決めること（D1〜D5） | D1（閲覧者で出し分け）・D2（`is_advertise` は全体広告の表示設定）・D3（併用）・D5（閲覧者のプラン）は決定。D4 は未決定 |
| Phase 1: 広告の表示 | 完了。PR 1-2（詳細画面の個別広告）・1-3（クリック数）は #989、PR 1-1（全体広告）は #1140 と閲覧者での出し分けの PR。PR 1-4（自動再生）は D2 で不要になった |
| Phase 2: ユーザーページ | 完了（#990・#991：投稿内検索、#993・#995：広告タブ） |
| Phase 3: Google Tag Manager | D4 待ち |
| Phase 4: 音楽ダウンロードのプラン制限 | 完了（#994。FE は既存の `download` を使うため変更なし） |
| Phase 5: 小さいもの | 音量の保存・決済キャンセル画面を対応 |
| Phase 6: 旧実装の撤去 | 完了（PR 6-1：削除の障壁 B1〜B3、PR 6-2：旧実装の削除） |
