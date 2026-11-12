from myus.domain.user.data import UserAllData
from myus.domain.user.interface import UserInterface
from myus.injectors.container import injector
from myus.utils.common.result import FatalError, Result
from myus.utils.functions.common import create_url
from ..dto.user import AuthorDTO


@Result.shield_exception()
def get_author_data(user_id: int) -> Result[AuthorDTO, FatalError]:
    author_map_ret = get_author_map_data([user_id])
    if author_map_ret.is_err:
        return Result.err(author_map_ret.err_value)

    author_map = author_map_ret.ok_value
    return Result.ok(author_map[user_id])


@Result.shield_exception()
def get_author_map_data(ids: list[int]) -> Result[dict[int, AuthorDTO], FatalError]:
    if len(ids) == 0:
        return Result.ok({})

    repo = injector.get(UserInterface)
    ret = repo.bulk_get(ids)
    if ret.is_err:
        return Result.err(ret.err_value)

    authors = ret.ok_value
    author_map: dict[int, AuthorDTO] = {id: AuthorDTO(avatar="", ulid="", nickname="", follower_count=0) for id in ids}
    for author in authors:
        author_map[author.user.id] = AuthorDTO(
            avatar=create_url(author.user.avatar),
            ulid=author.user.ulid,
            nickname=author.user.nickname,
            follower_count=author.mypage.follower_count,
        )

    return Result.ok(author_map)


@Result.shield_exception()
def save_user_data(data: UserAllData) -> Result[None, FatalError]:
    repo = injector.get(UserInterface)
    ret = repo.bulk_save([data])
    if ret.is_err:
        return Result.err(ret.err_value)

    return Result.ok(None)
