import { LARGE_UPLOAD_TIMEOUT_MS, apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { AdvertiseUpdateIn } from 'types/internal/advertise'
import { VideoUpdateIn, AudioUpdateIn, HiresIn, BlogUpdateIn, ComicUpdateIn, PictureUpdateIn, ChatUpdateIn } from 'types/internal/media/input'
import { ErrorOut } from 'types/internal/other'
import { apiManageVideo, apiManageAudio, apiManageHires, apiManageBlog, apiManageComic, apiManagePicture, apiManageChat, apiManageAdvertise } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const putManageVideo = async (ulid: string, request: VideoUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('form').put(apiManageVideo(ulid), camelSnake(request)))
}

export const putManageAudio = async (ulid: string, request: AudioUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('form').put(apiManageAudio(ulid), camelSnake(request)))
}

export const putManageHires = async (ulid: string, request: HiresIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('form', LARGE_UPLOAD_TIMEOUT_MS).put(apiManageHires(ulid), camelSnake(request)))
}

export const putManageBlog = async (ulid: string, request: BlogUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('form').put(apiManageBlog(ulid), camelSnake(request)))
}

export const putManageComic = async (ulid: string, request: ComicUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('form').put(apiManageComic(ulid), camelSnake(request)))
}

export const putManagePicture = async (ulid: string, request: PictureUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('form').put(apiManagePicture(ulid), camelSnake(request)))
}

export const putManageChat = async (ulid: string, request: ChatUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').put(apiManageChat(ulid), camelSnake(request)))
}

export const putManageAdvertise = async (ulid: string, request: AdvertiseUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('form').put(apiManageAdvertise(ulid), camelSnake(request)))
}
