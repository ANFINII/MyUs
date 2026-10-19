import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { VideoDetailOut } from 'types/internal/media/output'
import { getVideo, postMediaRead } from 'api/internal/media/detail'
import { MediaType } from 'utils/constants/enum'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import VideoDetail from 'components/templates/media/video/detail'

const getDetail = async (ulid: string): Promise<VideoDetailOut> => {
  await postMediaRead({ ulid, mediaType: MediaType.Video })
  return await toQuery(getVideo(ulid))
}

export default function VideoDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery({ queryKey: queryKeys.mediaVideoDetail(ulid), queryFn: () => getDetail(ulid) })
  const queries = { data }

  return (
    <QueryCheck title="Video" queries={queries} fresh>
      {(props) => <VideoDetail {...props} />}
    </QueryCheck>
  )
}
