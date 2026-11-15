from dataclasses import dataclass
from myus.utils.constants.page import PAGE_SIZE


@dataclass(frozen=True, slots=True)
class PageOption:
    limit: int = PAGE_SIZE
    offset: int = 0
