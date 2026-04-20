import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { ComicUpdateIn, MusicUpdateIn, PictureUpdateIn, VideoUpdateIn } from 'types/internal/media/input'
import { ErrorOut } from 'types/internal/other'
import { apiManageComic, apiManageMusic, apiManagePicture, apiManageVideo } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const putManageVideo = async (ulid: string, request: VideoUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').put(apiManageVideo(ulid), camelSnake(request)))
}

export const putManageMusic = async (ulid: string, request: MusicUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').put(apiManageMusic(ulid), camelSnake(request)))
}

export const putManageComic = async (ulid: string, request: ComicUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').put(apiManageComic(ulid), camelSnake(request)))
}

export const putManagePicture = async (ulid: string, request: PictureUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').put(apiManagePicture(ulid), camelSnake(request)))
}
