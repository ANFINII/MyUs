import { useQuery } from '@tanstack/react-query'
import { manageAdvertiseQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageAdvertiseEdit from 'components/templates/manage/advertise/edit'

export default function ManageAdvertiseEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery(manageAdvertiseQuery(ulid))
  const queries = { data }

  return (
    <QueryCheck title="Advertise" queries={queries}>
      {(props) => <ManageAdvertiseEdit {...props} />}
    </QueryCheck>
  )
}
