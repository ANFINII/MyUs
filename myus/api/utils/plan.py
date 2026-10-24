from dataclasses import dataclass
from api.utils.enum.user import PlanName


@dataclass(frozen=True, slots=True)
class PlanDef:
    name: str
    price: int
    max_advertise: int
    is_music_download: bool
    is_promotion: bool
    description: str


PLANS: list[PlanDef] = [
    PlanDef(
        name=PlanName.FREE,
        price=0,
        max_advertise=0,
        is_music_download=False,
        is_promotion=False,
        description="・有料プランを解約します\n・アップロード機能\n・コメント機能\n・フォロー機能など",
    ),
    PlanDef(
        name=PlanName.BASIC,
        price=550,
        max_advertise=1,
        is_music_download=False,
        is_promotion=True,
        description="・個別広告表示1つ\n・全体広告OFF\n・PR記事（アフィリエイト）",
    ),
    PlanDef(
        name=PlanName.STANDARD,
        price=880,
        max_advertise=2,
        is_music_download=False,
        is_promotion=True,
        description="・個別広告表示2つ\n・全体広告OFF\n・PR記事（アフィリエイト）",
    ),
    PlanDef(
        name=PlanName.PREMIUM,
        price=1200,
        max_advertise=3,
        is_music_download=True,
        is_promotion=True,
        description="・個別広告表示3つ\n・全体広告OFF\n・楽曲ダウンロード\n・PR記事（アフィリエイト）",
    ),
    PlanDef(
        name=PlanName.ULTIMATE,
        price=2000,
        max_advertise=4,
        is_music_download=True,
        is_promotion=True,
        description="・個別広告表示4つ\n・全体広告OFF\n・楽曲ダウンロード\n・PR記事（アフィリエイト）",
    ),
]


PLAN_MAP: dict[str, PlanDef] = {p.name: p for p in PLANS}


def get_plan(name: str) -> PlanDef | None:
    return PLAN_MAP.get(name)
