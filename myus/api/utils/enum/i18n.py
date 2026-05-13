from enum import Enum


class Currency(str, Enum):
    JPY = "Jpy"
    USD = "Usd"
    EUR = "Eur"
    GBP = "Gbp"
    CNY = "Cny"
    KRW = "Krw"


class Locale(str, Enum):
    JA = "Ja"
    EN = "En"
    ZH = "Zh"
    KO = "Ko"


class Country(str, Enum):
    JP = "Jp"
    US = "Us"
    GB = "Gb"
    CN = "Cn"
    KR = "Kr"
