from datetime import datetime, timedelta, date
from django.contrib.auth import get_user_model
from django.db.models import F, Count, Exists, OuterRef
from api.db.models import Plan, MyPage, SearchTag, UserNotification, Follow, Comment
from api.db.models import Video, Music, Comic, Picture, Blog, Chat, Advertise
from api.utils.constant import model_dict, model_media_comment_no_dict
from app.modules.notification import notification_data


User = get_user_model()


class ContextData:
    def context_data(self, class_name, **kwargs):
        context = super(class_name, self).get_context_data(**kwargs)
        user = self.request.user
        if user.id:
            notification = notification_data(user)
            context["notification_list"] = notification["notification_list"]
            context["notification_count"] = notification["notification_count"]
            context["searchtag_list"] = SearchTag.objects.filter(author=user).order_by("sequence")[:20]

        if hasattr(self, "count"):
            context["count"] = self.count or 0
            context["query"] = self.request.GET.get("search")

        class_name = str(class_name.__name__)
        if class_name == "UserNotificationView":
            context["user_notification"] = UserNotification.objects.filter(user=user.id).first()

        if class_name == "ProfileUpdate":
            context["gender"] = {"0":"男性", "1":"女性", "2":"秘密"}

        if class_name == "MyPageView":
            context["mypage_list"] = MyPage.objects.filter(user=user.id)

        if class_name == "Payment":
            context["payment_list"] = Plan.objects.all().order_by("-id")

        if class_name == "FollowList":
            context["follow_list"] = Follow.objects.filter(follower=user.id).select_related("following__mypage").order_by("created")[:100]

        if class_name == "FollowerList":
            context["follower_list"] = Follow.objects.filter(following=user.id).select_related("follower__mypage").order_by("created")[:100]

        if class_name == "Index":
            context.update({
                f"{value}_list": model.objects.filter(publish=True).order_by("-created")[:8]
                for model, value in model_dict.items()
            })

        if class_name == "Recommend":
            # 急上昇はcreatedが1日以内かつscoreが100000以上の上位8レコード
            # テストはcreatedが100日以内かつscoreが50以上の上位8レコード
            # socre = (read + like*10) + read * like/(read+1)*20
            aggregation_date = datetime.today() - timedelta(days=500)
            score = F("read") + Count("like")*10 + F("read")*Count("like")/(F("read")+1)*20
            context["Recommend"] = "Recommend"
            context.update({
                f"{value}_list": model.objects.annotate(score=score).filter(publish=True, created__gte=aggregation_date, score__gte=50).order_by("-score")[:8]
                for model, value in model_dict.items()
            })

        if class_name in ["UserPage", "UserPageInfo", "UserPageAdvertise"]:
            author = User.objects.get(nickname=self.kwargs["nickname"])
            follow = Follow.objects.filter(follower=user.id, following=author)
            context["is_follow"] = follow.exists()
            context["author"] = author
            context.update({
                f"{value}_list": model.objects.filter(author=author, publish=True).order_by("-created")
                for model, value in model_dict.items()
            })
        return context


    def models_context_data(self, class_name, **kwargs):
        context = super(class_name, self).get_context_data(**kwargs)
        user = self.request.user
        obj = self.object
        author = obj.author
        follow = Follow.objects.filter(follower=user.id, following=author)
        context["user_id"] = user.id
        context["obj_id"] = obj.id
        context["obj_path"] = self.request.path
        context["is_follow"] = follow.exists()

        if user.id:
            notification = notification_data(user)
            context["notification_list"] = notification["notification_list"]
            context["notification_count"] = notification["notification_count"]
            context["searchtag_list"] = SearchTag.objects.filter(author=user).order_by("sequence")[:20]

        context["advertise_auto_list"] = Advertise.objects.filter(publish=True, type=0).order_by("?")[:1]
        advertise = Advertise.objects.filter(publish=True, type=1, author=author).order_by("?")
        author_plan = author.user_plan.plan.name
        if author_plan == "Basic":
            context["advertise_list"] = advertise[:1]
        if author_plan == "Standard":
            context["advertise_list"] = advertise[:2]
        if author_plan == "Premium":
            context["advertise_list"] = advertise[:3]
        if author_plan == "Ultimate":
            context["advertise_list"] = advertise[:4]

        class_name = str(class_name.__name__)
        if class_name not in ["ChatDetail", "ChatThread"]:
            filter_subquery = dict(id=OuterRef("pk"), like__id=user.id)
            model_name = class_name.lower().split("detail")[0]
            filter_obj = dict(type_no=model_media_comment_no_dict[model_name], object_id=obj.id)
            subquery = Comment.objects.filter(**filter_subquery, **filter_obj)
            comment = Comment.objects.annotate(is_comment_like=Exists(subquery))
            context["comment_list"] = comment.filter(parent__isnull=True)
            context["reply_list"] = comment.filter(parent__isnull=False)

        if class_name == "VideoDetail":
            context["video_list"] = Video.objects.filter(publish=True).exclude(id=obj.id).order_by("-created")[:50]

        if class_name == "MusicDetail":
            context["music_list"] = Music.objects.filter(publish=True).exclude(id=obj.id).order_by("-created")[:50]

        if class_name == "ComicDetail":
            context["comic_list"] = Comic.objects.filter(publish=True).exclude(id=obj.id).order_by("-created")[:50]

        if class_name == "PictureDetail":
            context["picture_list"] = Picture.objects.filter(publish=True).exclude(id=obj.id).order_by("-created")[:50]

        if class_name == "BlogDetail":
            context["blog_list"] = Blog.objects.filter(publish=True).exclude(id=obj.id).order_by("-created")[:50]

        if class_name == "ChatDetail":
            context["is_period"] = obj.period < date.today()
            context["message_list"] = obj.message.filter(parent__isnull=True).select_related("author")
            context["chat_list"] = Chat.objects.filter(publish=True).exclude(id=obj.id).order_by("-created")[:50]

        if class_name == "ChatThread":
            message_id = self.kwargs["message_id"]
            context["message_id"] = message_id
            context["message_parent"] = obj.message.filter(id=message_id)
            context["is_period"] = obj.period < date.today()
            context["message_list"] = obj.message.filter(parent__isnull=True).select_related("author")
            context["reply_list"] = obj.message.filter(parent_id=message_id).select_related("author")
            context["chat_list"] = Chat.objects.filter(publish=True).exclude(id=obj.id).order_by("-created")[:50]

        return context
