import { useSuspenseQuery } from '@tanstack/react-query'
import { manageAdvertiseQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import ManageAdvertiseEdit from './view'

export default function ManageAdvertiseEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const { data } = useSuspenseQuery(manageAdvertiseQuery(ulid))

  return <ManageAdvertiseEdit data={data} />
}
