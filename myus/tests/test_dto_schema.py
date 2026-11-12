from dataclasses import fields
from typing import Any
import pytest
from pydantic import BaseModel
from myus.types.dto.advertise import AdvertiseInDTO
from myus.types.dto.media import VideoCreateDTO, MusicCreateDTO, BlogCreateDTO, ComicCreateDTO, PictureCreateDTO, ChatCreateDTO
from myus.types.dto.media import VideoUpdateDTO, MusicUpdateDTO, BlogUpdateDTO, ComicUpdateDTO, PictureUpdateDTO, ChatUpdateDTO
from myus.types.schema.advertise import AdvertiseIn, AdvertiseUpdateIn
from myus.types.schema.media.input import VideoIn, MusicIn, BlogIn, ComicIn, PictureIn, ChatIn
from myus.types.schema.media.input import VideoUpdateIn, MusicUpdateIn, BlogUpdateIn, ComicUpdateIn, PictureUpdateIn, ChatUpdateIn


# adapter で XxxDTO(**input.model_dump()) と組み替える組（項目の名前がずれると、実行したときに TypeError になる）
SCHEMA_DTO_PAIRS: list[tuple[type[BaseModel], Any]] = [
    (VideoIn, VideoCreateDTO),
    (MusicIn, MusicCreateDTO),
    (BlogIn, BlogCreateDTO),
    (ComicIn, ComicCreateDTO),
    (PictureIn, PictureCreateDTO),
    (ChatIn, ChatCreateDTO),
    (VideoUpdateIn, VideoUpdateDTO),
    (MusicUpdateIn, MusicUpdateDTO),
    (BlogUpdateIn, BlogUpdateDTO),
    (ComicUpdateIn, ComicUpdateDTO),
    (PictureUpdateIn, PictureUpdateDTO),
    (ChatUpdateIn, ChatUpdateDTO),
    (AdvertiseIn, AdvertiseInDTO),
    (AdvertiseUpdateIn, AdvertiseInDTO),
]


@pytest.mark.parametrize(("schema", "dto"), SCHEMA_DTO_PAIRS, ids=lambda cls: cls.__name__)
def test_dto_has_same_fields_as_schema(schema: type[BaseModel], dto: Any) -> None:
    assert set(schema.model_fields) == {field.name for field in fields(dto)}
