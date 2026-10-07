import { useQuery } from '@tanstack/react-query'
import { useParams } from '@tanstack/react-router'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getMusic } from 'api/internal/media/detail'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import MusicDetail from 'components/templates/media/music/detail'

export default function MusicDetailPage(): React.JSX.Element {
  const { ulid } = useParams({ from: '/media/music/$ulid' })

  const data = useQuery({ queryKey: queryKeys.mediaMusicDetail(ulid), queryFn: () => toQuery(getMusic(ulid)) })
  const queries = { data }

  return (
    <QueryCheck title="Music" queries={queries} fresh>
      {(props) => <MusicDetail {...props} />}
    </QueryCheck>
  )
}
