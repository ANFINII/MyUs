import { queryOptions } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { AdvertiseSearchParams } from 'types/internal/advertise'
import { SearchParams } from 'types/internal/media/output'
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
  getManageMusic,
  getManageMusics,
  getManagePicture,
  getManagePictures,
  getManageVideo,
  getManageVideos,
} from 'api/internal/manage/get'
import { getBlog, getComic, getMusic, getPicture, getVideo } from 'api/internal/media/detail'
import { getBlogs, getChats, getComics, getHome, getMusics, getPictures, getRecommend, getVideos } from 'api/internal/media/list'
import { getSettingMypage, getSettingNotification, getSettingProfile } from 'api/internal/setting'
import { getFollow, getFollower, getUser, getUserPage, getUserPageAdvertises, getUserPageMedia } from 'api/internal/user'

export const userQuery = () => queryOptions({ queryKey: queryKeys.user, queryFn: () => toQuery(getUser()), refetchOnMount: false })
export const channelsQuery = () => queryOptions({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()), refetchOnMount: false })
export const subscribeChannelsQuery = () => queryOptions({ queryKey: queryKeys.subscribeChannels, queryFn: () => toQuery(getSubscribeChannels()), refetchOnMount: false })
export const categoriesQuery = () => queryOptions({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()), refetchOnMount: false })

export const homeQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.home(params), queryFn: () => toQuery(getHome(params)), refetchOnMount: false })
export const recommendQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.recommend(params), queryFn: () => toQuery(getRecommend(params)), refetchOnMount: false })

export const videosQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaVideos(params), queryFn: () => toQuery(getVideos(params)), refetchOnMount: false })
export const musicsQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaMusics(params), queryFn: () => toQuery(getMusics(params)), refetchOnMount: false })
export const blogsQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaBlogs(params), queryFn: () => toQuery(getBlogs(params)), refetchOnMount: false })
export const comicsQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaComics(params), queryFn: () => toQuery(getComics(params)), refetchOnMount: false })
export const picturesQuery = (params: SearchParams) =>
  queryOptions({ queryKey: queryKeys.mediaPictures(params), queryFn: () => toQuery(getPictures(params)), refetchOnMount: false })
export const chatsQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaChats(params), queryFn: () => toQuery(getChats(params)), refetchOnMount: false })

export const videoQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaVideo(ulid), queryFn: () => toQuery(getVideo(ulid)), refetchOnMount: false })
export const musicQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaMusic(ulid), queryFn: () => toQuery(getMusic(ulid)), refetchOnMount: false })
export const blogQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaBlog(ulid), queryFn: () => toQuery(getBlog(ulid)), refetchOnMount: false })
export const comicQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaComic(ulid), queryFn: () => toQuery(getComic(ulid)), refetchOnMount: false })
export const pictureQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaPicture(ulid), queryFn: () => toQuery(getPicture(ulid)), refetchOnMount: false })

export const userPageQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.userPage(ulid), queryFn: () => toQuery(getUserPage(ulid)), refetchOnMount: false })
export const userPageMediaQuery = (ulid: string, channelUlid: string, params: SearchParams) =>
  queryOptions({ queryKey: queryKeys.userPageMedia(ulid, channelUlid, params), queryFn: () => toQuery(getUserPageMedia(ulid, channelUlid, params)), refetchOnMount: false })
export const userPageAdvertisesQuery = (ulid: string, params: SearchParams) =>
  queryOptions({ queryKey: queryKeys.userPageAdvertise(ulid, params), queryFn: () => toQuery(getUserPageAdvertises(ulid, params)), refetchOnMount: false })

export const followsQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.follows(params), queryFn: () => toQuery(getFollow(params)), refetchOnMount: false })
export const followersQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.followers(params), queryFn: () => toQuery(getFollower(params)), refetchOnMount: false })
export const settingProfileQuery = () => queryOptions({ queryKey: queryKeys.settingProfile, queryFn: () => toQuery(getSettingProfile()), refetchOnMount: false })
export const settingMypageQuery = () => queryOptions({ queryKey: queryKeys.settingMypage, queryFn: () => toQuery(getSettingMypage()), refetchOnMount: false })
export const settingNotificationQuery = () => queryOptions({ queryKey: queryKeys.settingNotification, queryFn: () => toQuery(getSettingNotification()), refetchOnMount: false })

export const manageVideosQuery = (params: SearchParams) =>
  queryOptions({ queryKey: queryKeys.manageVideos(params), queryFn: () => toQuery(getManageVideos(params)), refetchOnMount: false })
export const manageMusicsQuery = (params: SearchParams) =>
  queryOptions({ queryKey: queryKeys.manageMusics(params), queryFn: () => toQuery(getManageMusics(params)), refetchOnMount: false })
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
export const manageMusicQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.manageMusic(ulid), queryFn: () => toQuery(getManageMusic(ulid)), refetchOnMount: false })
export const manageBlogQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.manageBlog(ulid), queryFn: () => toQuery(getManageBlog(ulid)), refetchOnMount: false })
export const manageComicQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.manageComic(ulid), queryFn: () => toQuery(getManageComic(ulid)), refetchOnMount: false })
export const managePictureQuery = (ulid: string) =>
  queryOptions({ queryKey: queryKeys.managePicture(ulid), queryFn: () => toQuery(getManagePicture(ulid)), refetchOnMount: false })
export const manageChatQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.manageChat(ulid), queryFn: () => toQuery(getManageChat(ulid)), refetchOnMount: false })
export const manageAdvertiseQuery = (ulid: string) =>
  queryOptions({ queryKey: queryKeys.manageAdvertise(ulid), queryFn: () => toQuery(getManageAdvertise(ulid)), refetchOnMount: false })
