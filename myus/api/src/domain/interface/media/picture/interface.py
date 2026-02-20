from abc import ABC, abstractmethod
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, SortOption
from api.src.domain.interface.media.picture.data import PictureData


class PictureInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, limit: int | None = None) -> list[int]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[PictureData]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[PictureData]) -> None:
        ...
