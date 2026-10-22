import { noop, QueryClient } from '@tanstack/react-query'
import {
  blogDetailQuery,
  blogListQuery,
  channelsQuery,
  chatListQuery,
  comicDetailQuery,
  comicListQuery,
  followersQuery,
  followsQuery,
  homeQuery,
  musicDetailQuery,
  musicListQuery,
  pictureDetailQuery,
  pictureListQuery,
  recommendQuery,
  settingMypageQuery,
  settingNotificationQuery,
  settingProfileQuery,
  subscribeChannelsQuery,
  userQuery,
  videoDetailQuery,
  videoListQuery,
} from 'lib/query/options'
import { postMediaRead } from 'api/internal/media/read'
import { MediaType } from 'utils/constants/enum'
import { pageParams, searchParams } from 'utils/functions/common'

export interface PageLoad<TParams> {
  queryClient: QueryClient
  params: TParams
  search: Record<string, string>
}

const listParams = (query: Record<string, string>) => {
  const { search, limit, offset } = pageParams(query)
  return { search, limit, offset }
}

export const homeLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(homeQuery(searchParams(search))).catch(noop)
export const recommendLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(recommendQuery(searchParams(search))).catch(noop)
export const videoListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(videoListQuery(listParams(search))).catch(noop)
export const musicListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(musicListQuery(listParams(search))).catch(noop)
export const blogListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(blogListQuery(listParams(search))).catch(noop)
export const comicListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(comicListQuery(listParams(search))).catch(noop)
export const pictureListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(pictureListQuery(listParams(search))).catch(noop)
export const chatListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(chatListQuery(listParams(search))).catch(noop)

export const videoDetailLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Video })
  return queryClient.query(videoDetailQuery(params.ulid)).catch(noop)
}

export const musicDetailLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Music })
  return queryClient.query(musicDetailQuery(params.ulid)).catch(noop)
}

export const blogDetailLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Blog })
  return queryClient.query(blogDetailQuery(params.ulid)).catch(noop)
}

export const comicDetailLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Comic })
  return queryClient.query(comicDetailQuery(params.ulid)).catch(noop)
}

export const pictureDetailLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Picture })
  return queryClient.query(pictureDetailQuery(params.ulid)).catch(noop)
}

export const subscribeChannelsLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(subscribeChannelsQuery()).catch(noop)
export const followsLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(followsQuery(searchParams(search))).catch(noop)
export const followersLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(followersQuery(searchParams(search))).catch(noop)

export const settingProfileLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(settingProfileQuery()).catch(noop)
export const settingMypageLoader = ({ queryClient }: PageLoad<object>) => Promise.all([queryClient.query(settingMypageQuery()), queryClient.query(channelsQuery())]).catch(noop)
export const settingNotificationLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(settingNotificationQuery()).catch(noop)
export const settingPasswordLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(userQuery()).catch(noop)
export const settingPaymentLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(settingMypageQuery()).catch(noop)
