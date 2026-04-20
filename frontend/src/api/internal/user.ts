import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { SearchParms } from 'types/internal/media/output'
import { ErrorOut } from 'types/internal/other'
import { Follow, FollowIn, FollowOut, LikeCommentIn, LikeMediaIn, LikeOut, NotificationOut, SearchTagIn, SearchTagOut, UserMe } from 'types/internal/user'
import { UserPage, UserPageMedia } from 'types/internal/userpage'
import {
  apiFollow,
  apiFollower,
  apiFollowUser,
  apiLikeComment,
  apiLikeMedia,
  apiNotification,
  apiNotificationConfirmed,
  apiNotificationDeleted,
  apiSearchTag,
  apiUser,
  apiUserPage,
  apiUserPageMedia,
} from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const getUser = async (req?: Req): Promise<ApiOut<UserMe>> => {
  return await apiOut(apiClient('json').get(apiUser, cookieHeader(req)))
}

export const getSearchTag = async (req?: Req): Promise<ApiOut<SearchTagOut[]>> => {
  return await apiOut(apiClient('json').get(apiSearchTag, cookieHeader(req)))
}

export const putSearchTag = async (tags: SearchTagIn[]): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').put(apiSearchTag, camelSnake(tags)))
}

export const getFollow = async (params: SearchParms, req?: Req): Promise<ApiOut<Follow[]>> => {
  return await apiOut(apiClient('json').get(apiFollow, cookieHeader(req, params)))
}

export const getFollower = async (params: SearchParms, req?: Req): Promise<ApiOut<Follow[]>> => {
  return await apiOut(apiClient('json').get(apiFollower, cookieHeader(req, params)))
}

export const postFollow = async (request: FollowIn): Promise<ApiOut<FollowOut>> => {
  return await apiOut(apiClient('json').post(apiFollowUser, camelSnake(request)))
}

export const postLikeMedia = async (request: LikeMediaIn): Promise<ApiOut<LikeOut>> => {
  return await apiOut(apiClient('json').post(apiLikeMedia, camelSnake(request)))
}

export const postLikeComment = async (request: LikeCommentIn): Promise<ApiOut<LikeOut>> => {
  return await apiOut(apiClient('json').post(apiLikeComment, camelSnake(request)))
}

export const getNotification = async (req?: Req): Promise<ApiOut<NotificationOut>> => {
  return await apiOut(apiClient('json').get(apiNotification, cookieHeader(req)))
}

export const postNotificationConfirmed = async (ulid: string): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').post(apiNotificationConfirmed, camelSnake({ ulid })))
}

export const postNotificationDeleted = async (ulid: string): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').post(apiNotificationDeleted, camelSnake({ ulid })))
}

export const getUserPage = async (ulid: string, req?: Req): Promise<ApiOut<UserPage>> => {
  return await apiOut(apiClient('json').get(apiUserPage(ulid), cookieHeader(req)))
}

export const getUserPageMedia = async (ulid: string, channelUlid: string, req?: Req): Promise<ApiOut<UserPageMedia>> => {
  return await apiOut(apiClient('json').get(apiUserPageMedia(ulid, channelUlid), cookieHeader(req)))
}
