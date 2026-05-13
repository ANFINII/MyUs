# 決済基盤ロードマップ

## 目的

- 決済プロバイダ（現状 Stripe）に密結合させない汎用ドメインモデルを構築する
- 将来の **GMO ペイメント / Amazon Pay / Google Pay / PayPay** 等への切り替え・並行運用に耐える設計にする
- 将来 **User がマーチャントとして Store / Product を持ち課金できる**（Stripe Connect 等）構成に耐える設計にする
- 国際化（多通貨・多言語・複数国）対応の余地を残す
- `None` 多用ではなく **sum type / 状態 enum / value object** で型安全に表現する

## 進め方の原則

- **ドメイン層から先に設計** → 実装を後付けする
- 各 PR は **独立してマージ可能** な単位に切る
- 既存機能を壊さない（adapter / frontend 切替は最後にまとめて）
- mypy / lint / smoke test pass を必須

---

## 全体設計の最終形（参考）

実装は段階的に進めるが、最終的に到達したい形：

### 中心となるドメインモデル

```
User (買い手 / 売り手の両方になりうる)
  └─ Store (将来: User がマーチャントとして持つ店舗)
       └─ Product (将来: Store 配下の販売単位)
            └─ Price (将来: Product 配下の価格)

Subscription (継続課金の状態)
  ├─ customer_user_id        # 買い手
  ├─ seller_id               # 売り手（"" なら PLATFORM）
  ├─ provider                # PaymentProvider enum
  ├─ external_id             # プロバイダ固有 ID
  ├─ product_ref             # 内部商品参照
  ├─ price                   # Money value object
  ├─ status                  # SubscriptionStatus enum
  ├─ started_at
  ├─ current_period_end
  └─ canceled_at             # datetime.min なら未キャンセル

PaymentTransaction (個別取引)
  ├─ subscription_id         # 0 なら one-time
  ├─ customer_user_id
  ├─ provider
  ├─ external_id
  ├─ price                   # Money
  ├─ status                  # PaymentStatus enum
  └─ paid_at

WebhookEvent (プロバイダからの非同期通知)
  ├─ provider
  ├─ event_id                # 冪等性キー
  ├─ event_type              # WebhookEventType enum
  ├─ related_external_id
  └─ occurred_at
```

### Enum 群（最終形）

```python
class PaymentProvider(str, Enum):
    STRIPE = "Stripe"
    # 将来: GMO, AMAZON_PAY, PAYPAY, GOOGLE_PAY

class PaymentType(str, Enum):
    SUBSCRIPTION = "Subscription"
    ONE_TIME = "OneTime"

class Currency(str, Enum):
    JPY = "Jpy"
    USD = "Usd"
    EUR = "Eur"
    GBP = "Gbp"
    CNY = "Cny"
    KRW = "Krw"

class Locale(str, Enum):
    AUTO = "Auto"
    JA = "Ja"
    EN = "En"
    ZH = "Zh"
    KO = "Ko"

class Country(str, Enum):
    JP = "Jp"
    US = "Us"
    GB = "Gb"
    CN = "Cn"
    KR = "Kr"

class PaymentStatus(str, Enum):
    PENDING = "Pending"
    AUTHORIZED = "Authorized"
    CAPTURED = "Captured"
    FAILED = "Failed"
    REFUNDED = "Refunded"
    CANCELED = "Canceled"

class SubscriptionStatus(str, Enum):
    ACTIVE = "Active"
    PAST_DUE = "PastDue"
    CANCELED = "Canceled"
    EXPIRED = "Expired"
    INCOMPLETE = "Incomplete"

class WebhookEventType(str, Enum):
    PAYMENT_SUCCEEDED = "PaymentSucceeded"
    PAYMENT_FAILED = "PaymentFailed"
    SUBSCRIPTION_CREATED = "SubscriptionCreated"
    SUBSCRIPTION_UPDATED = "SubscriptionUpdated"
    SUBSCRIPTION_CANCELED = "SubscriptionCanceled"
    REFUND_ISSUED = "RefundIssued"

class CheckoutFailureReason(str, Enum):
    INVALID_PRODUCT_REF = "InvalidProductRef"
    INVALID_AMOUNT = "InvalidAmount"
    PROVIDER_ERROR = "ProviderError"
    PROVIDER_UNREACHABLE = "ProviderUnreachable"
```

### Value Object（プリミティブ裸渡しを禁じる）

```python
@dataclass(frozen=True, slots=True)
class Money:
    amount: int          # 最小単位（円なら円、ドルなら cents）
    currency: Currency

@dataclass(frozen=True, slots=True)
class CustomerData:
    email: str

@dataclass(frozen=True, slots=True)
class RedirectUrls:
    success_url: str
    cancel_url: str

@dataclass(frozen=True, slots=True)
class MarketplaceData:
    seller_id: str             # "" なら PLATFORM
    application_fee: Money     # Money(0, _) なら手数料無し
```

### CheckoutData / CheckoutResult

```python
@dataclass(frozen=True, slots=True)
class CheckoutData:
    payment_type: PaymentType
    price: Money
    customer: CustomerData
    description: str
    product_ref: str           # PlanName.value / 将来 Product.ulid
    redirect: RedirectUrls
    marketplace: MarketplaceData
    locale: Locale

@dataclass(frozen=True, slots=True)
class CheckoutSessionData:
    provider: PaymentProvider
    external_id: str
    redirect_url: str

@dataclass(frozen=True, slots=True)
class CheckoutCreated:
    session: CheckoutSessionData

@dataclass(frozen=True, slots=True)
class CheckoutFailed:
    reason: CheckoutFailureReason
    message: str

type CheckoutResult = CheckoutCreated | CheckoutFailed
```

### Provider Interface

```python
class PaymentProviderInterface(ABC):
    @abstractmethod
    def kind(self) -> PaymentProvider: ...

    @abstractmethod
    def create_checkout(self, input: CheckoutData) -> CheckoutResult: ...

    # 以下は Phase が進むごとに追加
    # def cancel_subscription(self, external_id: str) -> bool: ...
    # def get_subscription(self, external_id: str) -> SubscriptionFetchResult: ...
    # def verify_webhook(self, payload: bytes, signature: str) -> WebhookVerifyResult: ...
    # def onboard_seller(self, ...) -> OnboardResult: ...
```

### 呼び出しイメージ（match-case で網羅）

```python
result = payment.create_checkout(CheckoutData(...))
match result:
    case CheckoutCreated(session=session):
        return 200, PaymentCheckoutOut(url=session.redirect_url)
    case CheckoutFailed(reason=reason, message=message):
        log.warning("Checkout failed", reason=reason.value, error=message)
        return 500, ErrorOut(message="決済セッションの作成に失敗しました!")
```

---

## PR 計画

### ⬜ PR #1: 決済ドメイン層を新設（interfaces + data + enums のみ）

**Goal**: 実装無しでドメイン層を全部入れる。既存機能は無変更（adapter / frontend / injector は触らない）。

**Scope**:
- `myus/api/utils/enum/index.py` に enum 群追加
  - `PaymentProvider` / `PaymentType` / `Currency` / `Locale` / `Country` / `CheckoutFailureReason`
- `myus/api/src/domain/interface/payment/__init__.py` 新規
- `myus/api/src/domain/interface/payment/data.py` 新規
  - Value Object: `Money` / `CustomerData` / `RedirectUrls` / `MarketplaceData`
  - Input: `CheckoutData`
  - Output: `CheckoutSessionData` / `CheckoutCreated` / `CheckoutFailed`
  - Sum type: `type CheckoutResult = CheckoutCreated | CheckoutFailed`
- `myus/api/src/domain/interface/payment/provider.py` 新規
  - `PaymentProviderInterface`（`kind()` + `create_checkout(input) -> CheckoutResult`）

**Out of scope**:
- 実装（StripeProvider）
- adapter / injector / env 変更
- frontend 変更

**Acceptance**:
- mypy / lint pass
- 既存テストが全部 pass（インターフェースを誰も使っていないので影響無し）
- `import` パスが他ドメインの規約に揃っている

---

### ⬜ PR #2: Stripe Provider 実装 + injector 登録 + env 追加

**Goal**: PR #1 で定義した interface に対する Stripe 実装を作る。adapter / frontend はまだ触らない。

**Scope**:
- `myus/api/src/adapter/external/__init__.py` 新規
- `myus/api/src/adapter/external/payment/__init__.py` 新規
- `myus/api/src/adapter/external/payment/stripe_provider.py` 新規
  - `kind()` → `PaymentProvider.STRIPE`
  - `create_checkout(input)`:
    - SUBSCRIPTION: `product_ref` (PlanName) → `STRIPE_PRICE_ID_*` を private map で lookup
    - ONE_TIME: `price_data` で動的価格
    - `marketplace.seller_id` 非空時に Stripe Connect Destination Charges
    - `locale` を Stripe checkout の `locale` パラメータに変換
    - 失敗時は `CheckoutFailed(reason, message)` を返す（例外を投げない）
- `myus/api/src/injectors/index.py` に `PaymentModule` 追加
- `myus/api/src/injectors/container.py` に `PaymentModule()` 登録
- `myus/config/env.py` に `stripe_price_id_basic/standard/premium/ultimate` 追加
- `myus/config/settings/base.py` に `STRIPE_PRICE_ID_*` 公開
- `myus/envs/sample.env` / `django.env` に env キー追加

**Out of scope**:
- adapter / frontend 変更

**Acceptance**:
- mypy pass
- `injector.get(PaymentProviderInterface)` が `StripeProvider` を返す smoke test
- 既存 `adapter/payment.py`（Stripe 直接呼び出しのまま）は無変更で動く

---

### ⬜ PR #3: adapter リファクタ + frontend を新インターフェース経由に切替

**Goal**: 既存の Stripe 直接呼び出し adapter を、新 provider 経由に置き換える。フロントは `stripeId` → `plan` 送信に変更。ここで動作切替が完了する。

**Scope**:
- `myus/api/src/types/schema/payment.py`: `stripe_id` → `plan`
- `myus/api/src/adapter/payment.py`:
  - `import stripe` 削除
  - `injector.get(PaymentProviderInterface)` 経由で provider 取得
  - `CheckoutData` を組み立て、`match-case` で `CheckoutResult` を分岐
  - プラン価格は `api.utils.plan.get_plan()` で解決
- `frontend/src/types/internal/payment.d.ts`: `stripeId` → `plan`
- `frontend/src/components/templates/setting/payment/index.tsx`: `plan` 送信
- `frontend/src/components/templates/setting/payment/PlanCard/index.tsx`: `stripeId` フィールド削除、`name === 'Free'` で購入ボタン制御
- `frontend/src/components/templates/setting/payment/plans.ts`: Stripe price ID ハードコード削除

**Acceptance**:
- 手動テストで購入フローが動く
- mypy / lint / smoke pass
- adapter / usecase / frontend に Stripe 固有用語（`stripe_id` / `price_xxx`）が残っていない

---

### ⬜ PR #4: Subscription / PaymentTransaction テーブル設計

**Goal**: 既存 `UserPlan` を `Subscription` に置き換え、`PaymentTransaction` を新設。`provider` カラムを必須化。

**Scope**:
- `db/models/payment.py` 新設（`Subscription`, `PaymentTransaction`）
- 既存 `UserPlan` データを `Subscription` に移行する migration
- `db/models/user.py` から `UserPlan` を削除
- `UserPlanHistory` を `SubscriptionEvent` 等に rename / 拡張
- domain interface に `SubscriptionData` / `PaymentTransactionData` 追加
- adapter（mypage 等）の `user.user_plan` 参照を `user.subscription` に置き換え

**Acceptance**:
- 既存ユーザーの UserPlan データが Subscription として保持される
- mypage / プラン表示が壊れていない

---

### ⬜ PR #5: Webhook 受信エンドポイント（署名検証 + 冪等性）

**Goal**: Stripe からの webhook を受けて Subscription / PaymentTransaction の status を更新できるようにする。

**Scope**:
- `WebhookEventType` / `PaymentStatus` / `SubscriptionStatus` enum 追加
- `PaymentProviderInterface.verify_webhook(payload, signature) -> WebhookVerifyResult` 追加
- `StripeProvider.verify_webhook` 実装
- adapter で webhook 受信エンドポイント新設
- 冪等性: `WebhookEvent` テーブル（`provider`, `event_id` で unique）で重複弾く
- usecase で Subscription/Payment status を更新

**Acceptance**:
- Stripe CLI の webhook forward で動作確認
- 同じ event を 2 回送っても 2 回処理されない

---

### ⬜ PR #6: cancel_subscription / get_subscription API

**Goal**: ユーザーがプラン解約できる。

**Scope**:
- `PaymentProviderInterface.cancel_subscription` 追加
- `StripeProvider.cancel_subscription` 実装
- adapter API（`POST /payment/cancel`）追加
- フロント解約ボタン

**Acceptance**:
- 解約後、webhook 経由で Subscription.status が `CANCELED` になる

---

### ⬜ PR #7: User の Merchant 化フィールド追加（Stripe Connect 準備）

**Goal**: User がマーチャントになれる準備。

**Scope**:
- `User.stripe_account_id` カラム追加（空文字なら未マーチャント）
- `Country` enum を実利用開始
- 関連 migration

**Acceptance**:
- 既存ユーザーは `stripe_account_id=""` で問題無く動作

---

### ⬜ PR #8: Stripe Connect onboarding API

**Goal**: User が Stripe Connect で merchant 登録できる。

**Scope**:
- `PaymentProviderInterface.onboard_seller(user, return_url, country) -> OnboardResult` 追加
- `StripeProvider.onboard_seller` 実装（Account 作成 → AccountLink 生成）
- adapter API（`POST /payment/onboard`）
- フロント onboarding 開始ボタン
- `User.stripe_account_id` 更新

**Acceptance**:
- Stripe Connect Dashboard でテストアカウントが作成できる

---

### ⬜ PR #9: Store / Product / Price テーブル

**Goal**: User がマーチャントとして商品を登録できる準備（テーブルのみ）。

**Scope**:
- `db/models/store.py` → `Store(owner_user_id, name, description, is_active, ...)`
- `db/models/product.py` → `Product(store_id, name, kind, external_id)` + `Price(product_id, amount, currency, interval, external_id)`
- 関連 domain interface / entity / migration

**Acceptance**:
- migration pass、テーブル作成
- adapter API はまだ作らない

---

### ⬜ PR #10: User Merchant の Product 同期 + Marketplace checkout

**Goal**: User が登録した商品で買い物される checkout フローを実装。

**Scope**:
- `PaymentProviderInterface.sync_product(product, price, owner_account_id) -> SyncResult` で Stripe 側に Product/Price 作成、`external_id` を DB に保存
- `CheckoutData.marketplace.seller_id` に `user.stripe_account_id` を埋めて checkout
- usecase / adapter の整備

**Acceptance**:
- User が登録した商品で実際に課金が成立する（テストモード）

---

### ⬜ PR #11: 複数 Provider 対応（GMO 等の受け皿）

**Goal**: Stripe 以外のプロバイダを追加した際に動くインジェクション・dispatch 機構を整備。

**Scope**:
- `injectors/index.py` を `dict[PaymentProvider, PaymentProviderInterface]` ベースに変更
- usecase で provider を選択（User 設定 or 契約毎）
- GMO の実装は入れない（インフラのみ）

**Acceptance**:
- Stripe binding が今と同様に動く
- 別 Provider 追加時の手順がドキュメント化されている

---

### ⬜ PR #12: 国際化対応（多言語表示・多通貨）

**Goal**: `Locale` を実 API として使い、ユーザーの言語で checkout ページを表示する。

**Scope**:
- フロントから `locale` を送信（or User 設定から取得）
- `StripeProvider` の `locale` パラメータに反映
- 多通貨対応（`Currency` を利用箇所拡張）

---

## 設計上の決定事項（参考メモ）

- **`None` 排除方針**: `| None` の代わりに sum type / sentinel 値（`""`, `0`, `datetime.min`）/ `Failed` バリアントで表現する
- **Value Object 強制**: `amount: int` 単独を関数引数に取らない。常に `Money` で包む
- **`provider` カラム**: Subscription / PaymentTransaction / WebhookEvent には必ず `PaymentProvider` enum を持たせる（後で振り返り可能に）
- **`external_id` opaque**: プロバイダ固有 ID は文字列として持つだけ。ドメイン側でパース・解釈しない
- **マーチャント = User**: 別 `Merchant` テーブルは作らない。User が `Store` を持ち、`Store` が `Product` を持つ
- **PLATFORM プラン**: 当面は `seller_id=""` のセンチネルで PLATFORM 課金を表現。Store/Product 移行は段階的に
- **マイグレーション**: `UserPlan` → `Subscription` への移行は PR #4 で集中して行う

---

## 次にやること

→ **PR #1**（決済ドメイン層を新設・実装無し）を開始する。

ブランチ案: `back_feat_payment_domain`
