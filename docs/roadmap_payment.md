# 決済基盤ロードマップ（残り）

決済の今の仕組み（Stripe・webhook・帳簿・Subscription 集約）は [myus.md](myus.md) の「決済システム」にある。ここには、まだ作っていないものだけを残す。

## 方針（決めたこと）

- **`None` を使わない**：`| None` の代わりに、判別共用体・初期値（`""`・`0`・`datetime.min`）・`Failed` の型で表す
- **金額は `Money` で包む**：`amount: int` を単独で関数の引数にしない
- **`provider` は `PaymentEvent`・`PaymentCustomer`・`PaymentPayout` だけが持つ**：サブスクリプション・取引は顧客からたどる
- **決済会社の ID（`external_id`）は文字列として持つだけ**：ドメインの側で中身を解釈しない
- **売り手は User**：別の `Merchant` テーブルは作らない。受け取り口座は `PaymentSeller`（User と口座 ID の対応）に持つ。MyUs のプランの課金は `seller_id=""` で表す

## ⏸ クリエイターが売る機能（Stripe Connect・Store・Product）

当面は作らない（2026-10-26 決定）。作るときは [roadmap_event_sourcing.md](roadmap_event_sourcing.md) の Phase 7（帳簿の集約）の後にし、`PaymentSeller`・`Store`・`Product` は最初から集約として作る。

| 順 | 内容 |
|---|---|
| 1 | `PaymentSeller` を足し、`Subscription.seller_id` をその参照にする。明細の種類に `Transfer`（クリエイターへの送金。−）・`TransferReversal`（返金に伴う送金の取り消し。＋）を足す（詳しくは myus.md の「クリエイターへの支払い」） |
| 2 | Stripe Connect の登録：`PaymentInterface.onboard_seller` と `POST /payment/onboard`、FE の登録ボタン |
| 3 | `Store`・`Product`・`Price` のテーブル |
| 4 | 商品を Stripe に同期し（`sync_product`）、`CheckoutData.marketplace.seller_id` に受け取り口座を入れて決済する |

## 🔶 多通貨

言語は対応済み（決済画面を表示中の言語で出し、支払い後もその言語のページに戻す）。多通貨（`Currency` を価格・決済に使う）は、着手するか未定。

## 確認が残っているもの

- 本物の Stripe（テスト環境）で `invoice.paid`・`charge.refunded`・`payout.paid` を通し、取引・明細・入金が正しく作られるかを確かめる
- Stripe CLI で `customer.subscription.*` を送り、`es_event` と `Subscription`・`UserPlan` が正しく作られるかを確かめる

## 別の決済会社を足すときの手順

1. `api/utils/enum/payment.py` の `PaymentProvider` に値を足す（DB の `provider` の選択肢も変わるので、マイグレーションを作る）
2. `api/src/adapter/external/payment/<provider>/` に `PaymentInterface` の実装（`provider.py`・`_convert.py`）を置く
3. `injectors/index.py` の `provide_payment_providers` の辞書に1行足す
4. `adapter/payment.py` に、その決済会社の webhook の入口（例：`/payment/webhook/gmo`）を足し、署名を取り出して `verify_webhook(PaymentProvider.XXX, payload, signature)` を呼ぶ
5. キーなどを `config/env.py` と `envs/sample.env` に足す
6. 新しく始める決済をその会社にするなら、`usecase/payment/core.py` の `CHECKOUT_PROVIDER` を変える（ユーザーや契約ごとに選ぶなら、そこを選ぶ処理に置き換える）

どの決済会社を使うかは、決済の画面の作成は `CHECKOUT_PROVIDER`、解約は顧客（`PaymentCustomer`）の `provider`、webhook は受けたイベントの `provider` で決まる。
