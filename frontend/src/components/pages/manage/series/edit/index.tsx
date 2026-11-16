import { useSuspenseQuery } from '@tanstack/react-query'
import { manageSeriesQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import ManageSeriesEdit from './view'

export default function ManageSeriesEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')
  const { data } = useSuspenseQuery(manageSeriesQuery(ulid))

  return <ManageSeriesEdit key={ulid} data={data} />
}
