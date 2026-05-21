from datetime import datetime
from pydantic import BaseModel


class PaymentCheckoutIn(BaseModel):
    plan: str


class PaymentCheckoutOut(BaseModel):
    url: str


class PaymentWebhookOut(BaseModel):
    message: str


class PaymentCancelOut(BaseModel):
    canceled_at: datetime
    period_end: datetime
