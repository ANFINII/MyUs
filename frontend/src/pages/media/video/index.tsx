import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getVideos } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Videos from 'components/templates/media/video/list'

export default function VideosPage(): React.JSX.Element {
  const router = useAppRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }

  const query = useQuery({ queryKey: queryKeys.mediaVideoList(params), queryFn: () => toQuery(getVideos(params)), enabled: router.isReady, placeholderData: keepPreviousData })
  const queries = { list: query }

  return (
    <QueryCheck title="Video" queries={queries}>
      {(props) => <Videos {...props} page={page} />}
    </QueryCheck>
  )
}
