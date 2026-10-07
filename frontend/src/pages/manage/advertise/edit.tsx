import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getManageAdvertise } from 'api/internal/manage/get'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageAdvertiseEdit from 'components/templates/manage/advertise/edit'

export default function ManageAdvertiseEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery({ queryKey: queryKeys.manageAdvertiseDetail(ulid), queryFn: () => toQuery(getManageAdvertise(ulid)) })
  const queries = { data }

  return (
    <QueryCheck title="Advertise" queries={queries} fresh>
      {(props) => <ManageAdvertiseEdit {...props} />}
    </QueryCheck>
  )
}
