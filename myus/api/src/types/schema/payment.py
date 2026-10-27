from datetime import datetime
from pydantic import BaseModel
from api.utils.enum.i18n import Locale


class PaymentCheckoutIn(BaseModel):
    plan: str
    locale: Locale


class PaymentCheckoutOut(BaseModel):
    url: str


class PaymentWebhookOut(BaseModel):
    message: str


class PaymentCancelOut(BaseModel):
    canceled_at: datetime
    period_end: datetime
