import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { MusicUpdateIn } from 'types/internal/media/input'
import { Music, SearchParams } from 'types/internal/media/output'
import { ErrorOut } from 'types/internal/other'
import { apiManageMusic, apiManageMusics } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const getManageMusics = async (params: SearchParams, req?: Req): Promise<ApiOut<Music[]>> => {
  return await apiOut(apiClient('json').get(apiManageMusics, cookieHeader(req, params)))
}

export const getManageMusic = async (ulid: string, req?: Req): Promise<ApiOut<Music>> => {
  return await apiOut(apiClient('json').get(apiManageMusic(ulid), cookieHeader(req)))
}

export const putManageMusic = async (ulid: string, request: MusicUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').put(apiManageMusic(ulid), camelSnake(request)))
}

export const deleteManageMusics = async (ulids: string[]): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiManageMusics, { data: { ulids } }))
}
