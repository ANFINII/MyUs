from datetime import date
from dataclasses import dataclass
from api.src.types.data.plan import PlanData


@dataclass(frozen=True, slots=True)
class UserData:
    id: int
    avatar: str
    ulid: str
    email: str
    username: str
    nickname: str
    is_active: bool
    is_staff: bool
    profile: ProfileData
    mypage: MyPageData
    user_plan: UserPlanData


@dataclass(frozen=True, slots=True)
class ProfileData:
    full_name: str
    last_name: str
    first_name: str
    gender: str
    birthday: date | None
    year: int
    month: int
    day: int
    age: int
    phone: str
    country_code: str
    postal_code: str
    prefecture: str
    city: str
    street: str
    introduction: str


@dataclass(frozen=True, slots=True)
class MyPageData:
    banner: str
    email: str
    content: str
    follower_count: int
    following_count: int
    tag_manager_id: str
    is_advertise: bool


@dataclass(frozen=True, slots=True)
class UserPlanData:
    plan: PlanData
    customer_id: str
    subscription: str
    is_paid: bool
    start_date: date | None
    end_date: date | None
