import { useSuspenseQuery } from '@tanstack/react-query'
import { manageMusicQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import ManageMusicLyric from './view'

export default function ManageMusicLyricPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')
  const { data } = useSuspenseQuery(manageMusicQuery(ulid))

  return <ManageMusicLyric key={ulid} data={data} />
}
