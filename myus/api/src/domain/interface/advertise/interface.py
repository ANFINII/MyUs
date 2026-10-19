from abc import ABC, abstractmethod
from api.src.domain.interface.advertise.data import AdvertiseData
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PageOption, SortOption
from api.utils.common.result import FatalError, Result


class AdvertiseInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, page: PageOption, user_id: int | None = None) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[AdvertiseData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[AdvertiseData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        ...

    @abstractmethod
    def count(self, filter: FilterOption) -> Result[int, FatalError]:
        ...
