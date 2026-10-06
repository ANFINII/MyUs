import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getManageAdvertises } from 'api/internal/manage/get'
import { pageParams } from 'utils/functions/common'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageAdvertises from 'components/templates/manage/advertise'

export default function ManageAdvertisesPage(): React.JSX.Element {
  const router = useAppRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }

  const list = useQuery({
    queryKey: queryKeys.manageAdvertiseList(params),
    queryFn: () => toQuery(getManageAdvertises(params)),
    enabled: router.isReady,
    placeholderData: keepPreviousData,
  })
  const queries = { list }

  return (
    <QueryCheck title="Advertise" queries={queries}>
      {(props) => <ManageAdvertises {...props} page={page} />}
    </QueryCheck>
  )
}
