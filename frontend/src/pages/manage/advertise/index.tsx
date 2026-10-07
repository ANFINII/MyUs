import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { useSearch } from '@tanstack/react-router'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getManageAdvertises } from 'api/internal/manage/get'
import { pageParams } from 'utils/functions/common'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageAdvertises from 'components/templates/manage/advertise'

export default function ManageAdvertisesPage(): React.JSX.Element {
  const query = useSearch({ strict: false })
  const { search, page, limit, offset } = pageParams(query)
  const params = { search, limit, offset }

  const data = useQuery({ queryKey: queryKeys.manageAdvertiseList(params), queryFn: () => toQuery(getManageAdvertises(params)), placeholderData: keepPreviousData })
  const queries = { data }

  return (
    <QueryCheck title="Advertise" queries={queries}>
      {(props) => <ManageAdvertises {...props} page={page} />}
    </QueryCheck>
  )
}
