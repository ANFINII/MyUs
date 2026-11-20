import { useSuspenseQuery } from '@tanstack/react-query'
import { audioQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import AudioDetail from './view'

export default function AudioDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')
  const { data } = useSuspenseQuery(audioQuery(ulid))

  return <AudioDetail key={ulid} data={data} />
}
