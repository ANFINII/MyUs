from pydantic import BaseModel


class PaymentCheckoutIn(BaseModel):
    stripe_id: str


class PaymentCheckoutOut(BaseModel):
    url: str
