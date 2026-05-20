from pydantic import BaseModel


class PaymentCheckoutIn(BaseModel):
    plan: str


class PaymentCheckoutOut(BaseModel):
    url: str


class PaymentWebhookOut(BaseModel):
    message: str
