from dataclasses import dataclass
from api.utils.enum.index import PlanName


@dataclass(frozen=True, slots=True)
class PlanDef:
    name: str
    price: int
    max_advertise: int
    description: str


PLANS: list[PlanDef] = [
    PlanDef(
        name=PlanName.FREE,
        price=0,
        max_advertise=0,
        description="・有料プランを解約します\n・アップロード機能\n・コメント機能\n・フォロー機能など",
    ),
    PlanDef(
        name=PlanName.BASIC,
        price=550,
        max_advertise=1,
        description="・個別広告表示1つ\n・全体広告OFF",
    ),
    PlanDef(
        name=PlanName.STANDARD,
        price=880,
        max_advertise=2,
        description="・個別広告表示2つ\n・全体広告OFF",
    ),
    PlanDef(
        name=PlanName.PREMIUM,
        price=1200,
        max_advertise=3,
        description="・個別広告表示3つ\n・全体広告OFF\n・楽曲ダウンロード",
    ),
]


PLAN_MAP: dict[str, PlanDef] = {p.name: p for p in PLANS}


def get_plan(name: str) -> PlanDef | None:
    return PLAN_MAP.get(name)
