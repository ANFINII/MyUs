from ..enum.payment import ProductType


def included_tax(amount: int, rate: int) -> int:
    tax = abs(amount) * rate // (100 + rate)
    return tax if amount >= 0 else -tax


def create_product_code(product_type: ProductType, ulid: str) -> str:
    return f"{product_type.value}:{ulid}"


def parse_product_code(product_code: str) -> tuple[ProductType | None, str]:
    value, _, ulid = product_code.partition(":")
    product_type = next((t for t in ProductType if t.value == value), None)
    return product_type, ulid
