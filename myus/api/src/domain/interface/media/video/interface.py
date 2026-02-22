from abc import ABC, abstractmethod
from api.src.domain.interface.media.index import ExcludeOption, FilterOption, SortOption
from api.src.domain.interface.media.video.data import VideoData


class VideoInterface(ABC):
    @abstractmethod
    def get_ids(self, filter: FilterOption, exclude: ExcludeOption, sort: SortOption, limit: int | None = None) -> list[int]:
        ...

    @abstractmethod
    def bulk_get(self, ids: list[int]) -> list[VideoData]:
        ...

    @abstractmethod
    def bulk_save(self, objs: list[VideoData]) -> list[int]:
        ...

    @abstractmethod
    def is_liked(self, media_id: int, user_id: int) -> bool:
        ...
