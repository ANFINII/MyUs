import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getVideo } from 'api/internal/media/detail'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import VideoDetail from 'components/templates/media/video/detail'

export default function VideoDetailPage(): React.JSX.Element {
  const router = useAppRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery({ queryKey: queryKeys.mediaVideoDetail(ulid), queryFn: () => toQuery(getVideo(ulid)) })
  const queries = { data }

  return (
    <QueryCheck title="Video" queries={queries} fresh>
      {(props) => <VideoDetail {...props} />}
    </QueryCheck>
  )
}
