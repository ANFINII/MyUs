from datetime import date
from dataclasses import dataclass
from api.types.data.plan import PlanData


@dataclass(frozen=True)
class UserData:
    avatar: str
    email: str
    nickname: str
    is_active: bool
    is_staff: bool


@dataclass(frozen=True, slots=True)
class ProfileData:
    last_name: str
    first_name: str
    birthday: str
    gender: str
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
    tag_manager_id: int
    is_advertise: bool


@dataclass(frozen=True)
class UserPlanData:
    plan: PlanData
    customer_id: str
    subscription: str
    is_paid: int
    start_date: int
    end_date: int


@dataclass(frozen=True)
class UserDTO:
    user: UserData
    profile: ProfileData
    maypage: MyPageData
    plan: UserPlanData

    def full_name(self):
        return self.profile.last_name + ' ' + self.profile.first_name

    def birthday(self):
        return self.profile.birthday

    def year(self):
        if self.birthday:
            return self.birthday.year

    def month(self):
        if self.birthday:
            return self.birthday.month

    def day(self):
        if self.birthday:
            return self.birthday.day

    def age(self):
        if self.birthday:
            birthday = self.birthday
            DAYS_IN_YEAR = 365.2425
            return int((date.today() - birthday).days / DAYS_IN_YEAR)

    def gender(self):
        return self.profile.gender

    def prefecture(self):
        return self.profile.prefecture

    def city(self):
        return self.profile.city

    def street(self):
        return self.profile.street

    def image(self):
        if self.avatar:
            return self.avatar.url

    def banner(self):
        if self.mypage.banner:
            return self.mypage.banner.url

    def plan_name(self):
        return self.plan.plan.name

    def plan_start_date(self):
        return self.plan.start_date

    def plan_end_date(self):
        return self.plan.end_date
