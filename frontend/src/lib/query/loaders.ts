import { noop, QueryClient } from '@tanstack/react-query'
import { blogDetailQuery, comicDetailQuery, homeQuery, musicDetailQuery, pictureDetailQuery, videoDetailQuery } from 'lib/query/options'
import { postMediaRead } from 'api/internal/media/read'
import { MediaType } from 'utils/constants/enum'
import { searchParams } from 'utils/functions/common'

export interface PageLoad<TParams> {
  queryClient: QueryClient
  params: TParams
  search: Record<string, string>
}

export const homeLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.query(homeQuery(searchParams(search))).catch(noop)

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
