from datetime import date
from django.core.mail import send_mail
from api.db.models.user import MyPage, Profile, User, UserPlan
from .type import MyPageData, ProfileData, UserData, UserPlanData


def full_name(profile: Profile) -> str:
    return profile.last_name + " " + profile.first_name


def age(birthday: date) -> int:
    DAYS_IN_YEAR = 365.2425
    return int((date.today() - birthday).days / DAYS_IN_YEAR)


def email_user(user: User, subject: str, message: str, from_email: str | None = None, **kwargs) -> None:
    send_mail(subject, message, from_email, [user.email], **kwargs)


def user_data(user: User) -> UserData:
    assert hasattr(user, "profile"), "Profile is required"
    assert hasattr(user, "mypage"), "Mypage is required"
    assert hasattr(user, "user_plan"), "User plan is required"

    return UserData(
        id=user.id,
        ulid=user.ulid,
        avatar=user.avatar.url,
        email=user.email,
        username=user.username,
        nickname=user.nickname,
        is_active=user.is_active,
        is_staff=user.is_staff,
        profile=profile_data(user.profile),
        mypage=mypage_data(user.mypage),
        user_plan=user_plan_data(user.user_plan),
    )


def profile_data(profile: Profile) -> ProfileData:
    assert profile.birthday is not None, "Birthday is required"

    return ProfileData(
        full_name=full_name(profile),
        last_name=profile.last_name,
        first_name=profile.first_name,
        gender=profile.gender,
        birthday=profile.birthday,
        year=profile.birthday.year,
        month=profile.birthday.month,
        day=profile.birthday.day,
        age=age(profile.birthday),
        phone=profile.phone,
        country_code=profile.country_code,
        postal_code=profile.postal_code,
        prefecture=profile.prefecture,
        city=profile.city,
        street=profile.street,
        introduction=profile.introduction,
    )


def mypage_data(mypage: MyPage) -> MyPageData:
    return MyPageData(
        banner=mypage.banner.url,
        email=mypage.email,
        content=mypage.content,
        follower_count=mypage.follower_count,
        following_count=mypage.following_count,
        tag_manager_id=mypage.tag_manager_id,
        is_advertise=mypage.is_advertise,
    )


def user_plan_data(user_plan: UserPlan) -> UserPlanData:
    return UserPlanData(
        plan=user_plan.plan.name,
        customer_id=user_plan.customer_id,
        subscription=user_plan.subscription,
        is_paid=user_plan.is_paid,
        start_date=user_plan.start_date,
        end_date=user_plan.end_date,
    )
