import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { Follow, FollowIn, FollowOut, NotificationOut, SearchTagOut } from 'types/internal/auth'
import { SearchParms } from 'types/internal/media'
import { apiFollow, apiFollower, apiNotification, apiSearchTag } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const getSearchTag = async (req?: Req): Promise<ApiOut<SearchTagOut[]>> => {
  return await apiOut(apiClient.get(apiSearchTag, cookieHeader(req)))
}

export const getFollow = async (params: SearchParms, req?: Req): Promise<ApiOut<Follow[]>> => {
  return await apiOut(apiClient.get(apiFollow, cookieHeader(req, params)))
}

export const getFollower = async (params: SearchParms, req?: Req): Promise<ApiOut<Follow[]>> => {
  return await apiOut(apiClient.get(apiFollower, cookieHeader(req, params)))
}

export const postFollow = async (request: FollowIn): Promise<ApiOut<FollowOut>> => {
  return await apiOut(apiClient.post(apiFollow, camelSnake(request)))
}

export const getNotification = async (req?: Req): Promise<ApiOut<NotificationOut>> => {
  return await apiOut(apiClient.get(apiNotification, cookieHeader(req)))
}
