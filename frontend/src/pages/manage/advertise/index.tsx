import { useQuery } from '@tanstack/react-query'
import { manageAdvertisesQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageAdvertises from 'components/templates/manage/advertise'

export default function ManageAdvertisesPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }
  const data = useQuery(manageAdvertisesQuery(params))
  const queries = { data }

  return (
    <QueryCheck title="Advertise" queries={queries}>
      {(props) => <ManageAdvertises {...props} page={page} />}
    </QueryCheck>
  )
}
