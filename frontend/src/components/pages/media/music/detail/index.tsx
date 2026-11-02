import { useSuspenseQuery } from '@tanstack/react-query'
import { musicQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import MusicDetail from './view'

export default function MusicDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const { data } = useSuspenseQuery(musicQuery(ulid))

  return <MusicDetail data={data} />
}
