import { useQuery } from '@tanstack/react-query'
import { videosQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Videos from 'components/templates/media/video/list'

export default function VideosPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }

  const data = useQuery(videosQuery(params))
  const queries = { data }

  return (
    <QueryCheck title="Video" queries={queries}>
      {(props) => <Videos {...props} page={page} />}
    </QueryCheck>
  )
}
