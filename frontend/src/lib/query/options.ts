import { queryOptions } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { SearchParams } from 'types/internal/media/output'
import { getVideo } from 'api/internal/media/detail'
import { getHome } from 'api/internal/media/list'

export const homeQuery = (params: SearchParams) => queryOptions({ queryKey: queryKeys.home(params), queryFn: () => toQuery(getHome(params)) })

export const videoDetailQuery = (ulid: string) => queryOptions({ queryKey: queryKeys.mediaVideoDetail(ulid), queryFn: () => toQuery(getVideo(ulid)) })
