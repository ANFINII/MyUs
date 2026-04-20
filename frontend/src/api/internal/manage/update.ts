import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { MusicUpdateIn, VideoUpdateIn } from 'types/internal/media/input'
import { ErrorOut } from 'types/internal/other'
import { apiManageMusic, apiManageVideo } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const putManageVideo = async (ulid: string, request: VideoUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').put(apiManageVideo(ulid), camelSnake(request)))
}

export const putManageMusic = async (ulid: string, request: MusicUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').put(apiManageMusic(ulid), camelSnake(request)))
}
