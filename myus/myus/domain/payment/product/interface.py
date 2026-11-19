from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from myus.utils.common.result import FatalError, Result
from myus.utils.enum.payment import ProductType
from .data import ProductData


class SortType(Enum):
    ID = auto()


@dataclass(frozen=True, slots=True)
class FilterOption:
    ulid: str = ""
    seller_id: int = 0
    product_type: ProductType | None = None
    object_ids: list[int] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class SortOption:
    is_asc: bool = True
    sort_type: SortType = SortType.ID


@dataclass(frozen=True, slots=True)
class PageOption:
    limit: int = 0
    offset: int = 0


class ProductInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, sort: SortOption, page: PageOption) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[ProductData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[ProductData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        ...
