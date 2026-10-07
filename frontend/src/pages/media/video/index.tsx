import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { useSearch } from '@tanstack/react-router'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getVideos } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Videos from 'components/templates/media/video/list'

export default function VideosPage(): React.JSX.Element {
  const query = useSearch({ strict: false })
  const { search, page, limit, offset } = pageParams(query)
  const params = { search, limit, offset }

  const data = useQuery({ queryKey: queryKeys.mediaVideoList(params), queryFn: () => toQuery(getVideos(params)), placeholderData: keepPreviousData })
  const queries = { data }

  return (
    <QueryCheck title="Video" queries={queries}>
      {(props) => <Videos {...props} page={page} />}
    </QueryCheck>
  )
}
