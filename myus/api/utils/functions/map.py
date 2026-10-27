from typing import assert_never
from api.utils.enum.i18n import Locale
from api.utils.enum.media import CommentType, CommentTypeNo, MediaType
from api.utils.enum.payment import PaymentStatus


def comment_type_map(type_no: CommentTypeNo) -> CommentType:
    return CommentType[type_no.name]


def comment_type_no_map(type_name: CommentType) -> CommentTypeNo:
    return CommentTypeNo[type_name.name]


def payment_status_rank(status: PaymentStatus) -> int:
    match status:
        case PaymentStatus.PENDING | PaymentStatus.AUTHORIZED | PaymentStatus.FAILED:
            return 0
        case PaymentStatus.CAPTURED:
            return 1
        case PaymentStatus.REFUNDED | PaymentStatus.CANCELED:
            return 2
        case _:
            assert_never(status)


def locale_path(locale: Locale) -> str:
    match locale:
        case Locale.JA | Locale.ZH | Locale.KO:
            return ""
        case Locale.EN:
            return "/en"
        case _:
            assert_never(locale)
