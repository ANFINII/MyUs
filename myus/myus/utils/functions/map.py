from typing import assert_never
from ..enum.i18n import Country, Currency, Locale
from ..enum.media import CommentType, CommentTypeNo, MediaType
from ..enum.payment import PaymentStatus, ProductType


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


def mail_locale(locale: Locale) -> Locale:
    match locale:
        case Locale.JA | Locale.ZH | Locale.KO:
            return Locale.JA
        case Locale.EN:
            return Locale.EN
        case _:
            assert_never(locale)


def country_currency(country: Country) -> Currency:
    match country:
        case Country.JP:
            return Currency.JPY
        case _:
            return Currency.USD


def product_media_type(product_type: ProductType) -> MediaType:
    match product_type:
        case ProductType.BLOG:
            return MediaType.BLOG
        case ProductType.MUSIC_HIRES:
            return MediaType.MUSIC
        case _:
            assert_never(product_type)
