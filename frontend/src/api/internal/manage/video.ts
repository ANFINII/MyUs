import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { VideoUpdateIn } from 'types/internal/media/input'
import { SearchParams, Video } from 'types/internal/media/output'
import { ErrorOut } from 'types/internal/other'
import { apiManageVideo, apiManageVideos } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const getManageVideos = async (params: SearchParams, req?: Req): Promise<ApiOut<Video[]>> => {
  return await apiOut(apiClient('json').get(apiManageVideos, cookieHeader(req, params)))
}

export const getManageVideo = async (ulid: string, req?: Req): Promise<ApiOut<Video>> => {
  return await apiOut(apiClient('json').get(apiManageVideo(ulid), cookieHeader(req)))
}

export const putManageVideo = async (ulid: string, request: VideoUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').put(apiManageVideo(ulid), camelSnake(request)))
}

export const deleteManageVideos = async (ulids: string[]): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiManageVideos, { data: { ulids } }))
}
