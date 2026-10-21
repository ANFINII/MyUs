from abc import ABC, abstractmethod
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PageOption, SortOption
from api.src.domain.interface.media.comic.data import ComicData
from api.utils.common.result import FatalError, Result


class ComicInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, page: PageOption, user_id: int | None = None) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> Result[list[ComicData], FatalError]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[ComicData]) -> Result[list[int], FatalError]:
        ...

    @abstractmethod
    def bulk_delete(self, ids: list[int]) -> Result[None, FatalError]:
        ...

    @abstractmethod
    def count(self, filter: FilterOption) -> Result[int, FatalError]:
        ...

    @abstractmethod
    def is_liked(self, media_id: int, user_id: int) -> Result[bool, FatalError]:
        ...

    @abstractmethod
    def save_read(self, media_id: int) -> Result[int, FatalError]:
        ...
