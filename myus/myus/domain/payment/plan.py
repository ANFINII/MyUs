from dataclasses import dataclass
from myus.utils.enum.i18n import Currency
from myus.utils.enum.user import PlanName
from .data import Money


@dataclass(frozen=True, slots=True)
class Plan:
    name: str
    prices: list[Money]
    max_advertise: int
    is_music_download: bool
    is_playlist: bool
    is_series: bool
    is_hide_global_advertise: bool
    description: str


PLANS: list[Plan] = [
    Plan(
        name=PlanName.FREE,
        prices=[Money(amount=0, currency=Currency.JPY), Money(amount=0, currency=Currency.USD)],
        max_advertise=0,
        is_music_download=False,
        is_playlist=False,
        is_series=False,
        is_hide_global_advertise=False,
        description="・有料プランを解約します\n・アップロード機能\n・コメント機能\n・フォロー機能など",
    ),
    Plan(
        name=PlanName.BASIC,
        prices=[Money(amount=550, currency=Currency.JPY), Money(amount=399, currency=Currency.USD)],
        max_advertise=1,
        is_music_download=False,
        is_playlist=True,
        is_series=True,
        is_hide_global_advertise=False,
        description="・シリーズ作成\n・プレイリスト作成\n・個別広告表示1つ",
    ),
    Plan(
        name=PlanName.STANDARD,
        prices=[Money(amount=880, currency=Currency.JPY), Money(amount=599, currency=Currency.USD)],
        max_advertise=2,
        is_music_download=False,
        is_playlist=True,
        is_series=True,
        is_hide_global_advertise=True,
        description="・シリーズ作成\n・プレイリスト作成\n・個別広告表示2つ\n・全体広告非表示",
    ),
    Plan(
        name=PlanName.PREMIUM,
        prices=[Money(amount=1200, currency=Currency.JPY), Money(amount=799, currency=Currency.USD)],
        max_advertise=3,
        is_music_download=True,
        is_playlist=True,
        is_series=True,
        is_hide_global_advertise=True,
        description="・シリーズ作成\n・プレイリスト作成\n・個別広告表示3つ\n・全体広告非表示\n・楽曲ダウンロード",
    ),
    Plan(
        name=PlanName.ULTIMATE,
        prices=[Money(amount=2000, currency=Currency.JPY), Money(amount=1299, currency=Currency.USD)],
        max_advertise=4,
        is_music_download=True,
        is_playlist=True,
        is_series=True,
        is_hide_global_advertise=True,
        description="・シリーズ作成\n・プレイリスト作成\n・個別広告表示4つ\n・全体広告非表示\n・楽曲ダウンロード",
    ),
]


PLAN_MAP: dict[str, Plan] = {p.name: p for p in PLANS}


def get_plan(name: str) -> Plan | None:
    return PLAN_MAP.get(name)


def plan_price(plan: Plan, currency: Currency) -> Money:
    return next(p for p in plan.prices if p.currency == currency)
