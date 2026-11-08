def included_tax(amount: int, rate: int) -> int:
    tax = abs(amount) * rate // (100 + rate)
    return tax if amount >= 0 else -tax
