from abc import ABC, abstractmethod
from typing import Any
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, SortOption
from api.src.domain.interface.media.comic.data import ComicData


class ComicInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, limit: int | None = None) -> list[int]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[ComicData]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[ComicData]) -> list[ComicData]:
        ...

    @abstractmethod
    def create(self, **kwargs: Any) -> ComicData:
        ...
