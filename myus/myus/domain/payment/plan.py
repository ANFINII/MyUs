from dataclasses import dataclass
from myus.utils.enum.i18n import Currency
from myus.utils.enum.user import PlanName
from .data import Money


@dataclass(frozen=True, slots=True)
class Plan:
    name: str
    prices: list[Money]
    max_advertise: int
    is_playlist: bool
    is_series: bool
    is_hide_global_advertise: bool
    is_paid_content: bool
    is_long_hires: bool
    description: str


PLANS = [
    Plan(
        name=PlanName.FREE,
        prices=[Money(amount=0, currency=Currency.JPY), Money(amount=0, currency=Currency.USD)],
        max_advertise=0,
        is_playlist=False,
        is_series=False,
        is_hide_global_advertise=False,
        is_paid_content=False,
        is_long_hires=False,
        description="・有料プランを解約します\n・アップロード機能\n・コメント機能\n・フォロー機能など",
    ),
    Plan(
        name=PlanName.BASIC,
        prices=[Money(amount=550, currency=Currency.JPY), Money(amount=400, currency=Currency.USD)],
        max_advertise=1,
        is_playlist=True,
        is_series=True,
        is_hide_global_advertise=False,
        is_paid_content=False,
        is_long_hires=False,
        description="・シリーズ作成\n・プレイリスト作成 2つ\n・個別広告表示 1つ",
    ),
    Plan(
        name=PlanName.STANDARD,
        prices=[Money(amount=1100, currency=Currency.JPY), Money(amount=800, currency=Currency.USD)],
        max_advertise=2,
        is_playlist=True,
        is_series=True,
        is_hide_global_advertise=True,
        is_paid_content=True,
        is_long_hires=False,
        description="・シリーズ作成\n・プレイリスト作成\n・個別広告表示 2つ\n・全体広告非表示\n・有料記事・オーディオの販売",
    ),
    Plan(
        name=PlanName.PREMIUM,
        prices=[Money(amount=1650, currency=Currency.JPY), Money(amount=1200, currency=Currency.USD)],
        max_advertise=3,
        is_playlist=True,
        is_series=True,
        is_hide_global_advertise=True,
        is_paid_content=True,
        is_long_hires=True,
        description="・シリーズ作成\n・プレイリスト作成\n・個別広告表示 3つ\n・全体広告非表示\n・有料記事・オーディオの販売\n・1時間以上のハイレゾの販売",
    ),
    Plan(
        name=PlanName.ULTIMATE,
        prices=[Money(amount=3300, currency=Currency.JPY), Money(amount=2400, currency=Currency.USD)],
        max_advertise=4,
        is_playlist=True,
        is_series=True,
        is_hide_global_advertise=True,
        is_paid_content=True,
        is_long_hires=True,
        description="・シリーズ作成\n・プレイリスト作成\n・個別広告表示 4つ\n・全体広告非表示\n・有料記事・オーディオの販売\n・1時間以上のハイレゾの販売",
    ),
]


PLAN_MAP = {p.name: p for p in PLANS}


def get_plan(name: str) -> Plan | None:
    return PLAN_MAP.get(name)


def is_plan_available(plan: Plan, is_ultimate_invited: bool) -> bool:
    return plan.name != PlanName.ULTIMATE or is_ultimate_invited


def plan_price(plan: Plan, currency: Currency) -> Money:
    return next(p for p in plan.prices if p.currency == currency)
