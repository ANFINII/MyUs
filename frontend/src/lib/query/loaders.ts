import { QueryClient } from '@tanstack/react-query'
import { homeQuery, videoDetailQuery } from 'lib/query/options'
import { postMediaRead } from 'api/internal/media/read'
import { MediaType } from 'utils/constants/enum'
import { searchParams } from 'utils/functions/common'

export interface PageLoad<TParams> {
  queryClient: QueryClient
  params: TParams
  search: Record<string, string>
}

export const homeLoader = ({ queryClient, search }: PageLoad<object>) => queryClient.prefetchQuery(homeQuery(searchParams(search)))

export const videoDetailLoader = ({ queryClient, params }: PageLoad<{ ulid: string }>) => {
  postMediaRead({ ulid: params.ulid, mediaType: MediaType.Video })
  return queryClient.prefetchQuery(videoDetailQuery(params.ulid))
}
