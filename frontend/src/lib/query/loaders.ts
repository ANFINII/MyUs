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
  paymentPlansQuery,
  paymentSubscriptionQuery,
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
}

const listParams = (query: Record<string, string>) => {
  const { search, limit, offset } = pageParams(query)
  return { search, limit, offset }
}

const manageListParams = async (queryClient: QueryClient, search: Record<string, string>) => {
  const channels = await queryClient.query(channelsQuery())
  return { ...listParams(search), channel: search.channel || channels[0]?.ulid }
}

export const homeLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(homeQuery(searchParams(search)))
export const recommendLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(recommendQuery(searchParams(search)))
export const videoListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(videosQuery(listParams(search)))
export const musicListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(musicsQuery(listParams(search)))
export const blogListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(blogsQuery(listParams(search)))
export const comicListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(comicsQuery(listParams(search)))
export const pictureListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(picturesQuery(listParams(search)))
export const chatListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(chatsQuery(listParams(search)))

export const videoDetailLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Video })
  return queryClient.query(videoQuery(params.ulid))
}

export const musicDetailLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Music })
  return queryClient.query(musicQuery(params.ulid))
}

export const blogDetailLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Blog })
  return queryClient.query(blogQuery(params.ulid))
}

export const comicDetailLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Comic })
  return queryClient.query(comicQuery(params.ulid))
}

export const pictureDetailLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Picture })
  return queryClient.query(pictureQuery(params.ulid))
}

export const chatDetailLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Chat })
  return queryClient.query(chatQuery(params.ulid))
}

export const chatThreadLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => queryClient.query(chatQuery(params.ulid))

export const userPageLoader = ({ queryClient, params, search }: PageLoad<{ ulid: string }>) => {
  const query = searchParams(search)
  const userPage = queryClient.query(userPageQuery(params.ulid))
  const media = userPage
    .then((data) => {
      const channelUlid = selectChannelUlid(data.channels, search.channel)
      return channelUlid ? queryClient.query(userPageMediaQuery(params.ulid, channelUlid, query)) : undefined
    })
    .catch(noop)
  const advertises = queryClient.query(userPageAdvertisesQuery(params.ulid, query)).catch(noop)
  return Promise.all([userPage, media, advertises])
}

export const subscribeChannelsLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(subscribeChannelsQuery())
export const followsLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(followsQuery(searchParams(search)))
export const followersLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(followersQuery(searchParams(search)))

export const settingProfileLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(settingProfileQuery())
export const settingMypageLoader = ({ queryClient }: PageLoad<object>) => Promise.all([queryClient.query(settingMypageQuery()), queryClient.query(channelsQuery())])
export const settingNotificationLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(settingNotificationQuery())
export const settingPasswordLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(userQuery())
export const settingPaymentLoader = ({ queryClient }: PageLoad<object>) => Promise.all([queryClient.query(settingMypageQuery()), queryClient.query(settingProfileQuery()), queryClient.query(paymentSubscriptionQuery()), queryClient.query(paymentPlansQuery())])

export const manageLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(userQuery())
export const manageVideoListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageVideosQuery(await manageListParams(queryClient, search)))
export const manageMusicListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageMusicsQuery(await manageListParams(queryClient, search)))
export const manageBlogListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageBlogsQuery(await manageListParams(queryClient, search)))
export const manageComicListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageComicsQuery(await manageListParams(queryClient, search)))
export const managePictureListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(managePicturesQuery(await manageListParams(queryClient, search)))
export const manageChatListLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageChatsQuery(await manageListParams(queryClient, search)))
export const manageAdvertiseListLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageAdvertisesQuery(listParams(search)))
export const manageCreateLoader = ({ queryClient }: PageLoad<object>) => Promise.all([queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())])

export const manageVideoEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(manageVideoQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())])
export const manageMusicEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(manageMusicQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())])
export const manageBlogEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(manageBlogQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())])
export const manageComicEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(manageComicQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())])
export const managePictureEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(managePictureQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())])
export const manageChatEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => Promise.all([queryClient.query(manageChatQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())])
export const manageAdvertiseEditLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => queryClient.query(manageAdvertiseQuery(params.ulid))
