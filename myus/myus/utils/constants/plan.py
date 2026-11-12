from dataclasses import dataclass
from ..enum.user import PlanName


@dataclass(frozen=True, slots=True)
class Plan:
    name: str
    price: int
    max_advertise: int
    is_music_download: bool
    description: str


PLANS: list[Plan] = [
    Plan(
        name=PlanName.FREE,
        price=0,
        max_advertise=0,
        is_music_download=False,
        description="・有料プランを解約します\n・アップロード機能\n・コメント機能\n・フォロー機能など",
    ),
    Plan(
        name=PlanName.BASIC,
        price=550,
        max_advertise=1,
        is_music_download=False,
        description="・個別広告表示1つ\n・全体広告OFF",
    ),
    Plan(
        name=PlanName.STANDARD,
        price=880,
        max_advertise=2,
        is_music_download=False,
        description="・個別広告表示2つ\n・全体広告OFF",
    ),
    Plan(
        name=PlanName.PREMIUM,
        price=1200,
        max_advertise=3,
        is_music_download=True,
        description="・個別広告表示3つ\n・全体広告OFF\n・楽曲ダウンロード",
    ),
    Plan(
        name=PlanName.ULTIMATE,
        price=2000,
        max_advertise=4,
        is_music_download=True,
        description="・個別広告表示4つ\n・全体広告OFF\n・楽曲ダウンロード",
    ),
]


PLAN_MAP: dict[str, Plan] = {p.name: p for p in PLANS}


def get_plan(name: str) -> Plan | None:
    return PLAN_MAP.get(name)
