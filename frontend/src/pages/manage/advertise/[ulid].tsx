import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getManageAdvertise } from 'api/internal/manage/get'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageAdvertiseEdit from 'components/templates/manage/advertise/edit'

export default function ManageAdvertiseEditPage(): React.JSX.Element {
  const router = useAppRouter()
  const ulid = String(router.query.ulid ?? '')

  const query = useQuery({ queryKey: queryKeys.manageAdvertiseDetail(ulid), queryFn: () => toQuery(getManageAdvertise(ulid)), enabled: router.isReady })
  const queries = { data: query }

  return (
    <QueryCheck title="Advertise" queries={queries} fresh>
      {(props) => <ManageAdvertiseEdit {...props} />}
    </QueryCheck>
  )
}
