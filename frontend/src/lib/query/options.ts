import { queryOptions } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { AdvertiseSearchParams } from 'types/internal/advertise'
import { SearchParams } from 'types/internal/media/output'
import { getPasswordResetVerify, getSignupVerify } from 'api/internal/auth'
import { getCategories } from 'api/internal/category'
import { getChannels, getSubscribeChannels } from 'api/internal/channel'
import {
  getManageAdvertise,
  getManageAdvertises,
  getManageBlog,
  getManageBlogs,
  getManageChat,
  getManageChats,
  getManageComic,
  getManageComics,
  getManageAudio,
  getManageAudios,
  getManagePicture,
  getManagePictures,
  getManageVideo,
  getManageVideos,
} from 'api/internal/manage/get'
import { getManageSeries, getManageSeriesList } from 'api/internal/manage/series'
import { getBlog, getChat, getComic, getAudio, getPicture, getVideo } from 'api/internal/media/detail'
import { getBlogs, getChats, getComics, getHome, getAudios, getPictures, getVideos } from 'api/internal/media/list'
import { getPaymentPlans, getPaymentSeller, getPaymentSubscription } from 'api/internal/payment'
import { getPlaylist, getPlaylists, getUserPlaylists } from 'api/internal/playlist'
import { getChannelSeries } from 'api/internal/series'
import { getSettingMypage, getSettingNotification, getSettingProfile } from 'api/internal/setting'
import { getFollow, getFollower, getUser, getUserPage, getUserPageAdvertises, getUserPageMedia } from 'api/internal/user'

export const userQuery = () => queryOptions({ queryKey: queryKeys.user, queryFn: () => toQuery(getUser()), refetchOnMount: false })
export const signupQuery = (token: string) => queryOptions({ queryKey: queryKeys.signupVerify(token), queryFn: () => toQuery(getSignupVerify(token)) })
export const passwordResetQuery = (token: string) => queryOptions({ queryKey: queryKeys.passwordResetVerify(token), queryFn: () => toQuery(getPasswordResetVerify(token)) })
export const channelsQuery = () => queryOptions({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()), refetchOnMount: false })
export const subscribeChannelsQuery = () => queryOptions({ queryKey: queryKeys.subscribeChannels, queryFn: () => toQuery(getSubscribeChannels()), refetchOnMount: false })
export const categoriesQuery = () => queryOptions({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()), refetchOnMount: false })

export const homeQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.home(params), queryFn: () => toQuery(getHome(params)), refetchOnMount: false })

export const videosQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaVideos(params), queryFn: () => toQuery(getVideos(params)), refetchOnMount: false })
export const audiosQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaAudios(params), queryFn: () => toQuery(getAudios(params)), refetchOnMount: false })
export const blogsQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaBlogs(params), queryFn: () => toQuery(getBlogs(params)), refetchOnMount: false })
export const comicsQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaComics(params), queryFn: () => toQuery(getComics(params)), refetchOnMount: false })
export const picturesQuery = (params: SearchParams) =>
  queryOptions({ queryKey: queryKeys.mediaPictures(params), queryFn: () => toQuery(getPictures(params)), refetchOnMount: false })
export const chatsQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaChats(params), queryFn: () => toQuery(getChats(params)), refetchOnMount: false })

export const videoQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaVideo(ulid), queryFn: () => toQuery(getVideo(ulid)), refetchOnMount: false })
export const audioQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaAudio(ulid), queryFn: () => toQuery(getAudio(ulid)), refetchOnMount: false })
export const blogQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaBlog(ulid), queryFn: () => toQuery(getBlog(ulid)), refetchOnMount: false })
export const comicQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaComic(ulid), queryFn: () => toQuery(getComic(ulid)), refetchOnMount: false })
export const pictureQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaPicture(ulid), queryFn: () => toQuery(getPicture(ulid)), refetchOnMount: false })
export const chatQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaChat(ulid), queryFn: () => toQuery(getChat(ulid)), refetchOnMount: false })

export const playlistsQuery = () => queryOptions({ queryKey: queryKeys.mediaPlaylists, queryFn: () => toQuery(getPlaylists()), refetchOnMount: false })
export const playlistQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaPlaylist(ulid), queryFn: () => toQuery(getPlaylist(ulid)), refetchOnMount: false })

export const userPageQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.userPage(ulid), queryFn: () => toQuery(getUserPage(ulid)), refetchOnMount: false })
export const userPageMediaQuery = (ulid: string, channelUlid: string, params: SearchParams) =>
  queryOptions({ queryKey: queryKeys.userPageMedia(ulid, channelUlid, params), queryFn: () => toQuery(getUserPageMedia(ulid, channelUlid, params)), refetchOnMount: false })
export const userPageSeriesQuery = (ulid: string, channelUlid: string) =>
  queryOptions({ queryKey: queryKeys.userPageSeries(ulid, channelUlid), queryFn: () => toQuery(getChannelSeries(channelUlid)), refetchOnMount: false })
export const userPagePlaylistsQuery = (ulid: string) =>
  queryOptions({ queryKey: queryKeys.userPagePlaylists(ulid), queryFn: () => toQuery(getUserPlaylists(ulid)), refetchOnMount: false })
export const userPageAdvertisesQuery = (ulid: string, params: SearchParams) =>
  queryOptions({ queryKey: queryKeys.userPageAdvertise(ulid, params), queryFn: () => toQuery(getUserPageAdvertises(ulid, params)), refetchOnMount: false })

export const followsQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.follows(params), queryFn: () => toQuery(getFollow(params)), refetchOnMount: false })
export const followersQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.followers(params), queryFn: () => toQuery(getFollower(params)), refetchOnMount: false })
export const settingProfileQuery = () => queryOptions({ queryKey: queryKeys.settingProfile, queryFn: () => toQuery(getSettingProfile()), refetchOnMount: false })
export const settingMypageQuery = () => queryOptions({ queryKey: queryKeys.settingMypage, queryFn: () => toQuery(getSettingMypage()), refetchOnMount: false })
export const settingNotificationQuery = () => queryOptions({ queryKey: queryKeys.settingNotification, queryFn: () => toQuery(getSettingNotification()), refetchOnMount: false })
export const paymentSubscriptionQuery = () => queryOptions({ queryKey: queryKeys.paymentSubscription, queryFn: () => toQuery(getPaymentSubscription()), refetchOnMount: false })
export const paymentPlansQuery = () => queryOptions({ queryKey: queryKeys.paymentPlans, queryFn: () => toQuery(getPaymentPlans()), refetchOnMount: false })
export const paymentSellerQuery = () => queryOptions({ queryKey: queryKeys.paymentSeller, queryFn: () => toQuery(getPaymentSeller()), refetchOnMount: false })

export const manageVideosQuery = (params: SearchParams) =>
  queryOptions({ queryKey: queryKeys.manageVideos(params), queryFn: () => toQuery(getManageVideos(params)), refetchOnMount: false })
export const manageAudiosQuery = (params: SearchParams) =>
  queryOptions({ queryKey: queryKeys.manageAudios(params), queryFn: () => toQuery(getManageAudios(params)), refetchOnMount: false })
export const manageBlogsQuery = (params: SearchParams) =>
  queryOptions({ queryKey: queryKeys.manageBlogs(params), queryFn: () => toQuery(getManageBlogs(params)), refetchOnMount: false })
export const manageComicsQuery = (params: SearchParams) =>
  queryOptions({ queryKey: queryKeys.manageComics(params), queryFn: () => toQuery(getManageComics(params)), refetchOnMount: false })
export const managePicturesQuery = (params: SearchParams) =>
  queryOptions({ queryKey: queryKeys.managePictures(params), queryFn: () => toQuery(getManagePictures(params)), refetchOnMount: false })
export const manageChatsQuery = (params: SearchParams) =>
  queryOptions({ queryKey: queryKeys.manageChats(params), queryFn: () => toQuery(getManageChats(params)), refetchOnMount: false })
export const manageAdvertisesQuery = (params: AdvertiseSearchParams) =>
  queryOptions({ queryKey: queryKeys.manageAdvertises(params), queryFn: () => toQuery(getManageAdvertises(params)), refetchOnMount: false })

export const manageVideoQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.manageVideo(ulid), queryFn: () => toQuery(getManageVideo(ulid)), refetchOnMount: false })
export const manageAudioQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.manageAudio(ulid), queryFn: () => toQuery(getManageAudio(ulid)), refetchOnMount: false })
export const manageBlogQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.manageBlog(ulid), queryFn: () => toQuery(getManageBlog(ulid)), refetchOnMount: false })
export const manageComicQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.manageComic(ulid), queryFn: () => toQuery(getManageComic(ulid)), refetchOnMount: false })
export const managePictureQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.managePicture(ulid), queryFn: () => toQuery(getManagePicture(ulid)), refetchOnMount: false })
export const manageChatQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.manageChat(ulid), queryFn: () => toQuery(getManageChat(ulid)), refetchOnMount: false })
export const manageSeriesListQuery = (channelUlid: string) =>
  queryOptions({ queryKey: queryKeys.manageSeriesList(channelUlid), queryFn: () => toQuery(getManageSeriesList(channelUlid)), refetchOnMount: false })
export const manageSeriesQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.manageSeries(ulid), queryFn: () => toQuery(getManageSeries(ulid)), refetchOnMount: false })
export const manageAdvertiseQuery = (ulid: string) =>
  queryOptions({ queryKey: queryKeys.manageAdvertise(ulid), queryFn: () => toQuery(getManageAdvertise(ulid)), refetchOnMount: false })
