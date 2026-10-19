import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { MusicDetailOut } from 'types/internal/media/output'
import { getMusic } from 'api/internal/media/detail'
import { postMediaRead } from 'api/internal/media/read'
import { MediaType } from 'utils/constants/enum'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import MusicDetail from 'components/templates/media/music/detail'

const getDetail = async (ulid: string): Promise<MusicDetailOut> => {
  await postMediaRead({ ulid, mediaType: MediaType.Music })
  return await toQuery(getMusic(ulid))
}

export default function MusicDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery({ queryKey: queryKeys.mediaMusicDetail(ulid), queryFn: () => getDetail(ulid) })
  const queries = { data }

  return (
    <QueryCheck title="Music" queries={queries} fresh>
      {(props) => <MusicDetail {...props} />}
    </QueryCheck>
  )
}
