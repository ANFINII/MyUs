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
| 1 | メディア詳細の広告表示（全体広告 1 件 ＋ 投稿者の個別広告をプランに応じて 1〜4 件） | 未移行 | `app/modules/context_data.py:94-104`、`templates/parts/common/common.html:84-95` | `frontend/src/components/widgets/Advertise/index.tsx` は空の枠だけ。`isAd` を渡している所がなく表示されない |
| 2 | 広告のクリック数カウント | API のみ | `url/read` → `advertise_read` | `POST /advertise/{ulid}/read` はあるが、FE の `postAdvertiseRead` は未使用 |
| 3 | 全体広告（`type="all"`） | 未移行 | `Advertise.objects.filter(publish=True, type=0).order_by("?")[:1]` | 取得する API も FE も無い |
| 4 | 広告の自動再生設定（`is_advertise`） | 一部 | `advertise_article_auto.html` | 設定画面で保存はできるが、広告を出していないので効いていない |
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
| D2 | 全体広告の自動再生（`is_advertise`）は閲覧者の設定か、投稿者の設定か（旧実装は閲覧者のマイページ設定） | Phase 1 |
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

- BE：Stripe の cancel_url にキャンセルを示すクエリ（例：`?canceled=1`）を付ける（`adapter/payment.py`）
- FE：`/setting/payment` でクエリを見てトーストを出す

---

## Phase 6: 旧実装の撤去

Phase 1〜5（または対象外と決めたもの）が終わってから。

### PR 6-1【back】チャットの WebSocket ルーティングを api 側に移す

- `config/asgi.py` が `app/routing.py` を参照しているため、そのまま `app/` を消すとチャットの WebSocket が動かなくなる
- ルーティング（と consumer）を `api` 配下に移し、`config/asgi.py` の参照先を変える
- 完了条件：新しい FE のチャットがリアルタイム更新される

### PR 6-2【back】旧実装のルーティングとテンプレートを削除する

- `config/urls.py` の `path("", include("app.urls"))` を外す
- `myus/app/`・`myus/templates/`・旧実装専用の `static/` を削除
- `api/utils/functions/` などで旧実装からしか使われていない関数も削除
- 完了条件：mypy pass、`manage.py check` pass、FE の全画面が動く

---

## 進捗

| フェーズ | 状況 |
|---|---|
| 決めること（D1〜D5） | 未着手 |
| Phase 1: 広告の表示 | 未着手 |
| Phase 2: ユーザーページ | 未着手 |
| Phase 3: Google Tag Manager | 未着手 |
| Phase 4: 音楽ダウンロードのプラン制限 | 未着手 |
| Phase 5: 小さいもの | 未着手 |
| Phase 6: 旧実装の撤去 | 未着手 |
