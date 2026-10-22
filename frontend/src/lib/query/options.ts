import { queryOptions } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { AdvertiseSearchParams } from 'types/internal/advertise'
import { SearchParams } from 'types/internal/media/output'
import { getCategories } from 'api/internal/category'
import { getChannels, getSubscribeChannels } from 'api/internal/channel'
import { getManageAdvertise, getManageAdvertises, getManageBlog, getManageBlogs, getManageChat, getManageChats, getManageComic, getManageComics, getManageMusic, getManageMusics, getManagePicture, getManagePictures, getManageVideo, getManageVideos } from 'api/internal/manage/get'
import { getBlog, getComic, getMusic, getPicture, getVideo } from 'api/internal/media/detail'
import { getBlogs, getChats, getComics, getHome, getMusics, getPictures, getRecommend, getVideos } from 'api/internal/media/list'
import { getSettingMypage, getSettingNotification, getSettingProfile } from 'api/internal/setting'
import { getFollow, getFollower, getUser } from 'api/internal/user'

export const userQuery = () => queryOptions({ queryKey: queryKeys.user, queryFn: () => toQuery(getUser()), refetchOnMount: false })

export const channelsQuery = () => queryOptions({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()), refetchOnMount: false })

export const categoriesQuery = () => queryOptions({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()), refetchOnMount: false })

export const homeQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.home(params), queryFn: () => toQuery(getHome(params)), refetchOnMount: false })

export const recommendQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.recommend(params), queryFn: () => toQuery(getRecommend(params)), refetchOnMount: false })

export const videoListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaVideoList(params), queryFn: () => toQuery(getVideos(params)), refetchOnMount: false })

export const musicListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaMusicList(params), queryFn: () => toQuery(getMusics(params)), refetchOnMount: false })

export const blogListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaBlogList(params), queryFn: () => toQuery(getBlogs(params)), refetchOnMount: false })

export const comicListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaComicList(params), queryFn: () => toQuery(getComics(params)), refetchOnMount: false })

export const pictureListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaPictureList(params), queryFn: () => toQuery(getPictures(params)), refetchOnMount: false })

export const chatListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaChatList(params), queryFn: () => toQuery(getChats(params)), refetchOnMount: false })

export const videoDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaVideoDetail(ulid), queryFn: () => toQuery(getVideo(ulid)), refetchOnMount: false })

export const musicDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaMusicDetail(ulid), queryFn: () => toQuery(getMusic(ulid)), refetchOnMount: false })

export const blogDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaBlogDetail(ulid), queryFn: () => toQuery(getBlog(ulid)), refetchOnMount: false })

export const comicDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaComicDetail(ulid), queryFn: () => toQuery(getComic(ulid)), refetchOnMount: false })

export const pictureDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaPictureDetail(ulid), queryFn: () => toQuery(getPicture(ulid)), refetchOnMount: false })

export const subscribeChannelsQuery = () => queryOptions({ queryKey: queryKeys.subscribeChannels, queryFn: () => toQuery(getSubscribeChannels()), refetchOnMount: false })

export const followsQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.follows(params), queryFn: () => toQuery(getFollow(params)), refetchOnMount: false })

export const followersQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.followers(params), queryFn: () => toQuery(getFollower(params)), refetchOnMount: false })

export const settingProfileQuery = () => queryOptions({ queryKey: queryKeys.settingProfile, queryFn: () => toQuery(getSettingProfile()), refetchOnMount: false })

export const settingMypageQuery = () => queryOptions({ queryKey: queryKeys.settingMypage, queryFn: () => toQuery(getSettingMypage()), refetchOnMount: false })

export const settingNotificationQuery = () => queryOptions({ queryKey: queryKeys.settingNotification, queryFn: () => toQuery(getSettingNotification()), refetchOnMount: false })

export const manageVideoListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.manageVideoList(params), queryFn: () => toQuery(getManageVideos(params)), refetchOnMount: false })

export const manageMusicListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.manageMusicList(params), queryFn: () => toQuery(getManageMusics(params)), refetchOnMount: false })

export const manageBlogListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.manageBlogList(params), queryFn: () => toQuery(getManageBlogs(params)), refetchOnMount: false })

export const manageComicListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.manageComicList(params), queryFn: () => toQuery(getManageComics(params)), refetchOnMount: false })

export const managePictureListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.managePictureList(params), queryFn: () => toQuery(getManagePictures(params)), refetchOnMount: false })

export const manageChatListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.manageChatList(params), queryFn: () => toQuery(getManageChats(params)), refetchOnMount: false })

export const manageAdvertiseListQuery = (params: AdvertiseSearchParams) => queryOptions({ queryKey: queryKeys.manageAdvertiseList(params), queryFn: () => toQuery(getManageAdvertises(params)), refetchOnMount: false })

export const manageVideoDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.manageVideoDetail(ulid), queryFn: () => toQuery(getManageVideo(ulid)), refetchOnMount: false })

export const manageMusicDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.manageMusicDetail(ulid), queryFn: () => toQuery(getManageMusic(ulid)), refetchOnMount: false })

export const manageBlogDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.manageBlogDetail(ulid), queryFn: () => toQuery(getManageBlog(ulid)), refetchOnMount: false })

export const manageComicDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.manageComicDetail(ulid), queryFn: () => toQuery(getManageComic(ulid)), refetchOnMount: false })

export const managePictureDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.managePictureDetail(ulid), queryFn: () => toQuery(getManagePicture(ulid)), refetchOnMount: false })

export const manageChatDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.manageChatDetail(ulid), queryFn: () => toQuery(getManageChat(ulid)), refetchOnMount: false })

export const manageAdvertiseDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.manageAdvertiseDetail(ulid), queryFn: () => toQuery(getManageAdvertise(ulid)), refetchOnMount: false })
