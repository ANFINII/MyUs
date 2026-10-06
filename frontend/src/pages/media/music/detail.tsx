import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getMusic } from 'api/internal/media/detail'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import MusicDetail from 'components/templates/media/music/detail'

export default function MusicDetailPage(): React.JSX.Element {
  const router = useAppRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery({ queryKey: queryKeys.mediaMusicDetail(ulid), queryFn: () => toQuery(getMusic(ulid)), enabled: router.isReady })
  const queries = { data }

  return (
    <QueryCheck title="Music" queries={queries} fresh>
      {(props) => <MusicDetail {...props} />}
    </QueryCheck>
  )
}
