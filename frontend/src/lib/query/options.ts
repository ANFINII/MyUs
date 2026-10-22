import { queryOptions } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { SearchParams } from 'types/internal/media/output'
import { getBlog, getComic, getMusic, getPicture, getVideo } from 'api/internal/media/detail'
import { getBlogs, getChats, getComics, getHome, getMusics, getPictures, getRecommend, getVideos } from 'api/internal/media/list'

export const homeQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.home(params), queryFn: () => toQuery(getHome(params)), refetchOnMount: false })

export const recommendQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.recommend(params), queryFn: () => toQuery(getRecommend(params)), refetchOnMount: false })

export const videoDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaVideoDetail(ulid), queryFn: () => toQuery(getVideo(ulid)), refetchOnMount: false })

export const musicDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaMusicDetail(ulid), queryFn: () => toQuery(getMusic(ulid)), refetchOnMount: false })

export const blogDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaBlogDetail(ulid), queryFn: () => toQuery(getBlog(ulid)), refetchOnMount: false })

export const comicDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaComicDetail(ulid), queryFn: () => toQuery(getComic(ulid)), refetchOnMount: false })

export const pictureDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaPictureDetail(ulid), queryFn: () => toQuery(getPicture(ulid)), refetchOnMount: false })

export const videoListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaVideoList(params), queryFn: () => toQuery(getVideos(params)), refetchOnMount: false })

export const musicListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaMusicList(params), queryFn: () => toQuery(getMusics(params)), refetchOnMount: false })

export const blogListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaBlogList(params), queryFn: () => toQuery(getBlogs(params)), refetchOnMount: false })

export const comicListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaComicList(params), queryFn: () => toQuery(getComics(params)), refetchOnMount: false })

export const pictureListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaPictureList(params), queryFn: () => toQuery(getPictures(params)), refetchOnMount: false })

export const chatListQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.mediaChatList(params), queryFn: () => toQuery(getChats(params)), refetchOnMount: false })
