import { noop, QueryClient } from '@tanstack/react-query'
import {
  blogQuery,
  blogsQuery,
  categoriesQuery,
  channelsQuery,
  chatQuery,
  chatsQuery,
  comicQuery,
  comicsQuery,
  followersQuery,
  followsQuery,
  homeQuery,
  manageAdvertiseQuery,
  manageAdvertisesQuery,
  manageBlogQuery,
  manageBlogsQuery,
  manageChatQuery,
  manageChatsQuery,
  manageComicQuery,
  manageComicsQuery,
  manageMusicQuery,
  manageMusicsQuery,
  managePictureQuery,
  managePicturesQuery,
  manageVideoQuery,
  manageVideosQuery,
  musicQuery,
  musicsQuery,
  pictureQuery,
  picturesQuery,
  recommendQuery,
  settingMypageQuery,
  settingNotificationQuery,
  settingProfileQuery,
  subscribeChannelsQuery,
  userPageAdvertisesQuery,
  userPageMediaQuery,
  userPageQuery,
  userQuery,
  videoQuery,
  videosQuery,
} from 'lib/query/options'
import { postMediaRead } from 'api/internal/media/read'
import { MediaType } from 'utils/constants/enum'
import { selectChannelUlid } from 'utils/functions/channel'
import { pageParams, searchParams } from 'utils/functions/common'

export interface PageLoad<TParams> {
  queryClient: QueryClient
  params: TParams
  search: Record<string, string>
  from: string
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
export const videoListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(videosQuery(listParams(search))).catch(noop)
export const musicListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(musicsQuery(listParams(search))).catch(noop)
export const blogListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(blogsQuery(listParams(search))).catch(noop)
export const comicListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(comicsQuery(listParams(search))).catch(noop)
export const pictureListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(picturesQuery(listParams(search))).catch(noop)
export const chatListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(chatsQuery(listParams(search))).catch(noop)

export const videoDetailLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Video })
  return queryClient.query(videoQuery(params.ulid)).catch(noop)
}

export const musicDetailLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Music })
  return queryClient.query(musicQuery(params.ulid)).catch(noop)
}

export const blogDetailLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Blog })
  return queryClient.query(blogQuery(params.ulid)).catch(noop)
}

export const comicDetailLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Comic })
  return queryClient.query(comicQuery(params.ulid)).catch(noop)
}

export const pictureDetailLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Picture })
  return queryClient.query(pictureQuery(params.ulid)).catch(noop)
}

export const chatDetailLoader = ({ queryClient, params, from }: PageLoad<{ ulid: string }>) => {
  const chatPath = `/media/chat/${params.ulid}`
  if (from === chatPath || from.startsWith(`${chatPath}/`)) return Promise.resolve()
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Chat })
  return queryClient.query(chatQuery(params.ulid)).catch(noop)
}

export const userPageLoader = ({ queryClient, params, search }: PageLoad<{ ulid: string }>) => {
  const query = searchParams(search)
  const media = queryClient.query(userPageQuery(params.ulid)).then((userPage) => {
    const channelUlid = selectChannelUlid(userPage.channels, search.channel)
    return channelUlid ? queryClient.query(userPageMediaQuery(params.ulid, channelUlid, query)) : undefined
  })
  return Promise.all([media, queryClient.query(userPageAdvertisesQuery(params.ulid, query))]).catch(noop)
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
export const manageVideoListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageVideosQuery(await manageListParams(queryClient, search))).catch(noop)
export const manageMusicListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageMusicsQuery(await manageListParams(queryClient, search))).catch(noop)
export const manageBlogListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageBlogsQuery(await manageListParams(queryClient, search))).catch(noop)
export const manageComicListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageComicsQuery(await manageListParams(queryClient, search))).catch(noop)
export const managePictureListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(managePicturesQuery(await manageListParams(queryClient, search))).catch(noop)
export const manageChatListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageChatsQuery(await manageListParams(queryClient, search))).catch(noop)
export const manageAdvertiseListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageAdvertisesQuery(listParams(search))).catch(noop)
export const manageCreateLoader = ({ queryClient }: PageLoad<object>) => Promise.all([queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())]).catch(noop)

export const manageVideoEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(manageVideoQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())]).catch(noop)
export const manageMusicEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(manageMusicQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())]).catch(noop)
export const manageBlogEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(manageBlogQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())]).catch(noop)
export const manageComicEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(manageComicQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())]).catch(noop)
export const managePictureEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(managePictureQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())]).catch(noop)
export const manageChatEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(manageChatQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())]).catch(noop)
export const manageAdvertiseEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => queryClient.query(manageAdvertiseQuery(params.ulid)).catch(noop)
