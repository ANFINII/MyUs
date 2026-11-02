import { useSuspenseQuery } from '@tanstack/react-query'
import { videoQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import VideoDetail from './view'

export default function VideoDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')
  const { data } = useSuspenseQuery(videoQuery(ulid))

  return <VideoDetail data={data} />
}
