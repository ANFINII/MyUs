import { useQuery } from '@tanstack/react-query'
import { musicDetailQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import MusicDetail from 'components/templates/media/music/detail'

export default function MusicDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery(musicDetailQuery(ulid))
  const queries = { data }

  return (
    <QueryCheck title="Music" queries={queries}>
      {(props) => <MusicDetail {...props} />}
    </QueryCheck>
  )
}
