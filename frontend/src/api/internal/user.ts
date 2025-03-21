import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { Follow, NotificationOut, SearchTagOut } from 'types/internal/auth'
import { apiFollow, apiFollower, apiNotification, apiSearchTag } from 'api/uri'

export const getSearchTag = async (req?: Req): Promise<ApiOut<SearchTagOut[]>> => {
  return await apiOut(apiClient.get(apiSearchTag, cookieHeader(req)))
}

export const getFollow = async (req?: Req, search?: string): Promise<ApiOut<Follow[]>> => {
  return await apiOut(apiClient.get(apiFollow, cookieHeader(req, { search })))
}

export const getFollower = async (req?: Req, search?: string): Promise<ApiOut<Follow[]>> => {
  return await apiOut(apiClient.get(apiFollower, cookieHeader(req, { search })))
}

export const getNotification = async (req?: Req): Promise<ApiOut<NotificationOut>> => {
  return await apiOut(apiClient.get(apiNotification, cookieHeader(req)))
}
