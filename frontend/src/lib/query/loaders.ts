import { noop, QueryClient } from '@tanstack/react-query'
import {
  blogDetailQuery,
  blogListQuery,
  categoriesQuery,
  channelsQuery,
  chatListQuery,
  comicDetailQuery,
  comicListQuery,
  followersQuery,
  followsQuery,
  homeQuery,
  manageAdvertiseDetailQuery,
  manageAdvertiseListQuery,
  manageBlogDetailQuery,
  manageBlogListQuery,
  manageChatDetailQuery,
  manageChatListQuery,
  manageComicDetailQuery,
  manageComicListQuery,
  manageMusicDetailQuery,
  manageMusicListQuery,
  managePictureDetailQuery,
  managePictureListQuery,
  manageVideoDetailQuery,
  manageVideoListQuery,
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

const manageListParams = async (queryClient: QueryClient, search: Record<string, string>) => {
  const channels = await queryClient.query(channelsQuery()).catch(noop)
  return { ...listParams(search), channel: search.channel || channels?.[0]?.ulid }
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

export const manageLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(userQuery()).catch(noop)
export const manageVideoListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageVideoListQuery(await manageListParams(queryClient, search))).catch(noop)
export const manageMusicListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageMusicListQuery(await manageListParams(queryClient, search))).catch(noop)
export const manageBlogListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageBlogListQuery(await manageListParams(queryClient, search))).catch(noop)
export const manageComicListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageComicListQuery(await manageListParams(queryClient, search))).catch(noop)
export const managePictureListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(managePictureListQuery(await manageListParams(queryClient, search))).catch(noop)
export const manageChatListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageChatListQuery(await manageListParams(queryClient, search))).catch(noop)
export const manageAdvertiseListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageAdvertiseListQuery(listParams(search))).catch(noop)
export const manageCreateLoader = ({ queryClient }: PageLoad<object>) => Promise.all([queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())]).catch(noop)

export const manageVideoEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(manageVideoDetailQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())]).catch(noop)
export const manageMusicEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(manageMusicDetailQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())]).catch(noop)
export const manageBlogEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(manageBlogDetailQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())]).catch(noop)
export const manageComicEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(manageComicDetailQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())]).catch(noop)
export const managePictureEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(managePictureDetailQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())]).catch(noop)
export const manageChatEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(manageChatDetailQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())]).catch(noop)
export const manageAdvertiseEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => queryClient.query(manageAdvertiseDetailQuery(params.ulid)).catch(noop)
