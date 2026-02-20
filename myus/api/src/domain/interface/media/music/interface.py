from abc import ABC, abstractmethod
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, SortOption
from api.src.domain.interface.media.music.data import MusicData


class MusicInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, limit: int | None = None) -> list[int]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[MusicData]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[MusicData]) -> None:
        ...
