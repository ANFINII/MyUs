import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { SearchParams } from 'types/internal/media/output'
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

export const getUser = async (): Promise<ApiOut<UserMe>> => {
  return await apiOut(apiClient('json').get(apiUser))
}

export const getUserPage = async (ulid: string): Promise<ApiOut<UserPage>> => {
  return await apiOut(apiClient('json').get(apiUserPage(ulid)))
}

export const getUserPageMedia = async (ulid: string, channelUlid: string): Promise<ApiOut<UserPageMedia>> => {
  return await apiOut(apiClient('json').get(apiUserPageMedia(ulid, channelUlid)))
}

export const getSearchTag = async (): Promise<ApiOut<SearchTagOut[]>> => {
  return await apiOut(apiClient('json').get(apiSearchTag))
}

export const putSearchTag = async (tags: SearchTagIn[]): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').put(apiSearchTag, camelSnake(tags)))
}

export const getFollow = async (params: SearchParams): Promise<ApiOut<Follow[]>> => {
  return await apiOut(apiClient('json').get(apiFollow, { params }))
}

export const getFollower = async (params: SearchParams): Promise<ApiOut<Follow[]>> => {
  return await apiOut(apiClient('json').get(apiFollower, { params }))
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

export const getNotification = async (): Promise<ApiOut<NotificationOut>> => {
  return await apiOut(apiClient('json').get(apiNotification))
}

export const postNotificationConfirmed = async (ulid: string): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').post(apiNotificationConfirmed, camelSnake({ ulid })))
}

export const postNotificationDeleted = async (ulid: string): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').post(apiNotificationDeleted, camelSnake({ ulid })))
}
