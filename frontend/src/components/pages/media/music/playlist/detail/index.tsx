import { useSuspenseQuery } from '@tanstack/react-query'
import { playlistQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import PlaylistDetail from './view'

export default function PlaylistDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')
  const { data } = useSuspenseQuery(playlistQuery(ulid))

  return <PlaylistDetail key={ulid} data={data} />
}
