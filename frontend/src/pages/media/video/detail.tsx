import { useQuery } from '@tanstack/react-query'
import { videoDetailQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import VideoDetail from 'components/templates/media/video/detail'

export default function VideoDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery(videoDetailQuery(ulid))
  const queries = { data }

  return (
    <QueryCheck title="Video" queries={queries}>
      {(props) => <VideoDetail {...props} />}
    </QueryCheck>
  )
}
