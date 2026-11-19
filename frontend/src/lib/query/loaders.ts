import { noop, QueryClient } from '@tanstack/react-query'
import { redirect } from '@tanstack/react-router'
import { trackUserPageView } from 'lib/gtag'
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
  manageSeriesListQuery,
  manageSeriesQuery,
  manageVideoQuery,
  manageVideosQuery,
  musicQuery,
  musicsQuery,
  passwordResetQuery,
  paymentPlansQuery,
  paymentSellerQuery,
  paymentSubscriptionQuery,
  pictureQuery,
  picturesQuery,
  settingMypageQuery,
  settingNotificationQuery,
  settingProfileQuery,
  signupQuery,
  subscribeChannelsQuery,
  userPageAdvertisesQuery,
  userPageMediaQuery,
  userPagePlaylistsQuery,
  userPageSeriesQuery,
  userPageQuery,
  userQuery,
  videoQuery,
  videosQuery,
  playlistQuery,
  playlistsQuery,
} from 'lib/query/options'
import { postMediaRead } from 'api/internal/media/read'
import { MediaType } from 'utils/constants/enum'
import { selectChannelUlid } from 'utils/functions/channel'
import { homeParams, pageParams, searchParams } from 'utils/functions/common'

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

const verifyLoader = async <T>(token: string | undefined, load: (token: string) => Promise<T>): Promise<T> => {
  if (!token) throw redirect({ href: '/account/login' })
  try {
    return await load(token)
  } catch {
    throw redirect({ href: '/account/login' })
  }
}

export const signupLoader = ({ queryClient, search }: PageLoad<object>) => verifyLoader(search.token, (token) => queryClient.query(signupQuery(token)))
export const passwordResetLoader = ({ queryClient, search }: PageLoad<object>) => verifyLoader(search.token, (token) => queryClient.query(passwordResetQuery(token)))
export const withdrawalLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(userQuery())

export const homeLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(homeQuery(homeParams(search)))
export const videosLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(videosQuery(listParams(search)))
export const musicsLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(musicsQuery(listParams(search)))
export const blogsLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(blogsQuery(listParams(search)))
export const comicsLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(comicsQuery(listParams(search)))
export const picturesLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(picturesQuery(listParams(search)))
export const chatsLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(chatsQuery(listParams(search)))

export const videoLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Video })
  return queryClient.query(videoQuery(params.ulid))
}

export const musicLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Music })
  return queryClient.query(musicQuery(params.ulid))
}

export const blogLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Blog })
  return queryClient.query(blogQuery(params.ulid))
}

export const comicLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Comic })
  return queryClient.query(comicQuery(params.ulid))
}

export const pictureLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Picture })
  return queryClient.query(pictureQuery(params.ulid))
}

export const chatLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Chat })
  return queryClient.query(chatQuery(params.ulid))
}

export const chatThreadLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => queryClient.query(chatQuery(params.ulid))
export const playlistsLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(playlistsQuery())
export const playlistLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => queryClient.query(playlistQuery(params.ulid))

export const userPageLoader = ({ queryClient, params, search }: PageLoad<{ ulid: string }>) => {
  const query = searchParams(search)
  const userPage = queryClient.query(userPageQuery(params.ulid))
  userPage.then((data) => trackUserPageView(params.ulid, data.measurementId, `${data.nickname} - MyUs`)).catch(noop)
  const media = userPage
    .then((data) => {
      const channelUlid = selectChannelUlid(data.channels, search.channel)
      return channelUlid ? queryClient.query(userPageMediaQuery(params.ulid, channelUlid, query)) : undefined
    })
    .catch(noop)
  const series = userPage
    .then((data) => {
      const channelUlid = selectChannelUlid(data.channels, search.channel)
      return channelUlid ? queryClient.query(userPageSeriesQuery(params.ulid, channelUlid)) : undefined
    })
    .catch(noop)
  const playlists = queryClient.query(userPagePlaylistsQuery(params.ulid)).catch(noop)
  const advertises = queryClient.query(userPageAdvertisesQuery(params.ulid, query)).catch(noop)
  return Promise.all([userPage, media, series, playlists, advertises])
}

export const subscribeChannelsLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(subscribeChannelsQuery())
export const followsLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(followsQuery(searchParams(search)))
export const followersLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(followersQuery(searchParams(search)))

export const settingProfileLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(settingProfileQuery())
export const settingMypageLoader = ({ queryClient }: PageLoad<object>) => Promise.all([queryClient.query(settingMypageQuery()), queryClient.query(channelsQuery())])
export const settingNotificationLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(settingNotificationQuery())
export const settingPasswordLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(userQuery())
export const settingPaymentLoader = ({ queryClient }: PageLoad<object>) =>
  Promise.all([
    queryClient.query(settingMypageQuery()),
    queryClient.query(paymentSubscriptionQuery()),
    queryClient.query(paymentPlansQuery()),
    queryClient.query(paymentSellerQuery()),
  ])

export const manageLoader = ({ queryClient }: PageLoad<object>) => queryClient.query(userQuery())
export const manageCreateLoader = ({ queryClient }: PageLoad<object>) => Promise.all([queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())])
export const manageBlogCreateLoader = ({ queryClient }: PageLoad<object>) =>
  Promise.all([queryClient.query(channelsQuery()), queryClient.query(categoriesQuery()), queryClient.query(paymentSellerQuery())])

export const manageVideosLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageVideosQuery(await manageListParams(queryClient, search)))
export const manageMusicsLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageMusicsQuery(await manageListParams(queryClient, search)))
export const manageBlogsLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageBlogsQuery(await manageListParams(queryClient, search)))
export const manageComicsLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageComicsQuery(await manageListParams(queryClient, search)))
export const managePicturesLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(managePicturesQuery(await manageListParams(queryClient, search)))
export const manageChatsLoader = async ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageChatsQuery(await manageListParams(queryClient, search)))
export const manageAdvertisesLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(manageAdvertisesQuery(listParams(search)))
export const manageSeriesListLoader = async ({ queryClient, search }: PageLoad<object>) => {
  const channels = await queryClient.query(channelsQuery())
  return queryClient.query(manageSeriesListQuery(search.channel || channels[0]?.ulid || ''))
}

export const manageVideoLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) =>
  Promise.all([queryClient.query(manageVideoQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())])
export const manageMusicLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) =>
  Promise.all([queryClient.query(manageMusicQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())])
export const manageBlogLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) =>
  Promise.all([queryClient.query(manageBlogQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery()), queryClient.query(paymentSellerQuery())])
export const manageComicLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) =>
  Promise.all([queryClient.query(manageComicQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())])
export const managePictureLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) =>
  Promise.all([queryClient.query(managePictureQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())])
export const manageChatLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) =>
  Promise.all([queryClient.query(manageChatQuery(params.ulid)), queryClient.query(channelsQuery()), queryClient.query(categoriesQuery())])
export const manageAdvertiseLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => queryClient.query(manageAdvertiseQuery(params.ulid))
export const manageSeriesLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => queryClient.query(manageSeriesQuery(params.ulid))
