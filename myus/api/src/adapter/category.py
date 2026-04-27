from django.http import HttpRequest
from ninja import Router
from api.modules.logger import log
from api.src.types.schema.category import CategoryOut
from api.src.types.schema.common import ErrorOut
from api.src.usecase.auth import auth_check
from api.src.usecase.category import get_categories


class CategoryAPI:
    """CategoryAPI"""

    router = Router()

    @staticmethod
    @router.get("", response={200: list[CategoryOut], 401: ErrorOut})
    def get(request: HttpRequest):
        log.info("CategoryAPI get")

        user_id = auth_check(request)
        if user_id is None:
            return 401, ErrorOut(message="Unauthorized")

        categories = get_categories()
        return 200, [CategoryOut(ulid=c.ulid, jp_name=c.jp_name, en_name=c.en_name) for c in categories]
