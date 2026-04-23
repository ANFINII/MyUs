from abc import ABC, abstractmethod
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, PageOption, SortOption
from api.src.domain.interface.media.picture.data import PictureData


class PictureInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, page: PageOption, user_id: int | None = None) -> list[int]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[PictureData]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[PictureData]) -> list[int]:
        ...

    @abstractmethod
    def bulk_delete(self, ids: list[int]) -> None:
        ...

    @abstractmethod
    def count(self, filter: FilterOption) -> int:
        ...

    @abstractmethod
    def is_liked(self, media_id: int, user_id: int) -> bool:
        ...
