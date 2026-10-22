import { queryOptions } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { SearchParams } from 'types/internal/media/output'
import { getBlog, getComic, getMusic, getPicture, getVideo } from 'api/internal/media/detail'
import { getHome } from 'api/internal/media/list'

export const homeQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.home(params), queryFn: () => toQuery(getHome(params)), refetchOnMount: false })

export const videoDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaVideoDetail(ulid), queryFn: () => toQuery(getVideo(ulid)), refetchOnMount: false })

export const musicDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaMusicDetail(ulid), queryFn: () => toQuery(getMusic(ulid)), refetchOnMount: false })

export const blogDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaBlogDetail(ulid), queryFn: () => toQuery(getBlog(ulid)), refetchOnMount: false })

export const comicDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaComicDetail(ulid), queryFn: () => toQuery(getComic(ulid)), refetchOnMount: false })

export const pictureDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaPictureDetail(ulid), queryFn: () => toQuery(getPicture(ulid)), refetchOnMount: false })
