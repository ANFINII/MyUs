from abc import ABC, abstractmethod
from api.src.domain.interface.advertise.data import AdvertiseData
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PageOption, SortOption


class AdvertiseInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, page: PageOption, user_id: int | None = None) -> list[int]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[AdvertiseData]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[AdvertiseData]) -> list[int]:
        ...

    @abstractmethod
    def bulk_delete(self, ids: list[int]) -> None:
        ...

    @abstractmethod
    def count(self, filter: FilterOption) -> int:
        ...
