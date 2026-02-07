from django.contrib.auth.hashers import make_password
from api.db.models.master import Plan
from api.db.models.user import MyPage, Profile, User, UserNotification, UserPlan
from api.src.domain.interface.user.data import MyPageData, ProfileData, UserAllData, UserData, UserNotificationData, UserPlanData
from api.src.types.data.plan import PlanData


# Django model -> dataclass
def convert_data(user: User) -> UserAllData:
    assert hasattr(user, "profile"), "Profile is required"
    assert hasattr(user, "mypage"), "Mypage is required"
    assert hasattr(user, "notification"), "Notification is required"
    assert hasattr(user, "user_plan"), "User plan is required"

    return UserAllData(
        user=user_data(user),
        profile=profile_data(user.profile),
        mypage=mypage_data(user.mypage),
        notification=user_notification_data(user.notification),
        user_plan=user_plan_data(user.user_plan),
    )


def user_data(user: User) -> UserData:
    return UserData(
        id=user.id,
        ulid=user.ulid,
        avatar=user.avatar.name if user.avatar else "",
        password=user.password,
        email=user.email,
        username=user.username,
        nickname=user.nickname,
        is_active=user.is_active,
        is_staff=user.is_staff,
    )


def profile_data(profile: Profile) -> ProfileData:
    return ProfileData(
        last_name=profile.last_name,
        first_name=profile.first_name,
        gender=profile.gender,
        birthday=profile.birthday,
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
        banner=mypage.banner.name if mypage.banner else "",
        email=mypage.email,
        content=mypage.content,
        follower_count=mypage.follower_count,
        following_count=mypage.following_count,
        tag_manager_id=mypage.tag_manager_id,
        is_advertise=mypage.is_advertise,
    )


def user_notification_data(user_notification: UserNotification) -> UserNotificationData:
    return UserNotificationData(
        is_video=user_notification.is_video,
        is_music=user_notification.is_music,
        is_comic=user_notification.is_comic,
        is_picture=user_notification.is_picture,
        is_blog=user_notification.is_blog,
        is_chat=user_notification.is_chat,
        is_follow=user_notification.is_follow,
        is_reply=user_notification.is_reply,
        is_like=user_notification.is_like,
        is_views=user_notification.is_views,
    )


def plan_data(plan: Plan) -> PlanData:
    return PlanData(
        name=plan.name,
        stripe_api_id=plan.stripe_api_id,
        price=plan.price,
        max_advertise=plan.max_advertise,
        description=plan.description,
    )


def user_plan_data(user_plan: UserPlan) -> UserPlanData:
    return UserPlanData(
        plan=plan_data(user_plan.plan),
        customer_id=user_plan.customer_id,
        subscription=user_plan.subscription,
        is_paid=user_plan.is_paid,
        start_date=user_plan.start_date,
        end_date=user_plan.end_date,
    )


# dataclass -> Django model
def marshal_user(data: UserData) -> User:
    return User(
        id=data.id if data.id != 0 else None,
        ulid=data.ulid,
        avatar=data.avatar,
        password=make_password(data.password) if data.id == 0 else data.password,
        email=data.email,
        username=data.username,
        nickname=data.nickname,
        is_active=data.is_active,
    )


def marshal_profile(user: User, data: UserAllData) -> Profile:
    return Profile(
        user=user,
        last_name=data.profile.last_name,
        first_name=data.profile.first_name,
        gender=data.profile.gender,
        birthday=data.profile.birthday,
        phone=data.profile.phone,
        country_code=data.profile.country_code,
        postal_code=data.profile.postal_code,
        prefecture=data.profile.prefecture,
        city=data.profile.city,
        street=data.profile.street,
        introduction=data.profile.introduction,
    )


def marshal_mypage(user: User, data: UserAllData) -> MyPage:
    return MyPage(
        user=user,
        email=data.mypage.email,
        content=data.mypage.content,
        follower_count=data.mypage.follower_count,
        following_count=data.mypage.following_count,
        tag_manager_id=data.mypage.tag_manager_id,
        is_advertise=data.mypage.is_advertise,
    )


def marshal_notification(user: User, data: UserAllData) -> UserNotification:
    return UserNotification(
        user=user,
        is_video=data.notification.is_video,
        is_music=data.notification.is_music,
        is_comic=data.notification.is_comic,
        is_picture=data.notification.is_picture,
        is_blog=data.notification.is_blog,
        is_chat=data.notification.is_chat,
        is_follow=data.notification.is_follow,
        is_reply=data.notification.is_reply,
        is_like=data.notification.is_like,
        is_views=data.notification.is_views,
    )


def marshal_user_plan(user: User, data: UserAllData) -> UserPlan:
    return UserPlan(
        user=user,
        plan=user.user_plan.plan,
        customer_id=data.user_plan.customer_id,
        subscription=data.user_plan.subscription,
        is_paid=data.user_plan.is_paid,
        start_date=data.user_plan.start_date,
        end_date=data.user_plan.end_date,
    )
