from datetime import datetime
from pydantic import BaseModel
from myus.utils.enum.i18n import Currency, Locale


class PaymentCheckoutIn(BaseModel):
    plan: str
    locale: Locale


class PaymentChangeIn(BaseModel):
    plan: str


class PaymentMethodIn(BaseModel):
    locale: Locale


class PaymentCheckoutOut(BaseModel):
    url: str


class PaymentMethodOut(BaseModel):
    url: str


class PaymentWebhookOut(BaseModel):
    message: str


class PaymentCancelOut(BaseModel):
    canceled_at: datetime
    period_end: datetime


class PaymentSubscriptionOut(BaseModel):
    is_canceled: bool
    is_past_due: bool
    period_end: datetime


class MoneyOut(BaseModel):
    amount: int
    currency: Currency


class PaymentPlanOut(BaseModel):
    name: str
    price: MoneyOut
