from enum import Enum


class GenderType(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    SECRET = "Secret"


class PlanName(str, Enum):
    FREE = "Free"
    BASIC = "Basic"
    STANDARD = "Standard"
    PREMIUM = "Premium"
    ULTIMATE = "Ultimate"


class PlanAction(str, Enum):
    SUBSCRIBE = "Subscribe"
    CHANGE = "Change"
    CANCEL = "Cancel"
    EXPIRE = "Expire"
