import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getFollow } from 'api/internal/user'
import { searchParams } from 'utils/functions/common'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Follows from 'components/templates/menu/follow'

export default function FollowsPage(): React.JSX.Element {
  const router = useAppRouter()
  const params = searchParams(router.query)

  const datas = useQuery({ queryKey: queryKeys.follows(params), queryFn: () => toQuery(getFollow(params)), enabled: router.isReady, placeholderData: keepPreviousData })
  const queries = { datas }

  return (
    <QueryCheck title="Follow" queries={queries}>
      {(props) => <Follows {...props} />}
    </QueryCheck>
  )
}
