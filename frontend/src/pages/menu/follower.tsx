import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getFollower } from 'api/internal/user'
import { searchParams } from 'utils/functions/common'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Followers from 'components/templates/menu/follower'

export default function FollowersPage(): React.JSX.Element {
  const router = useAppRouter()
  const params = searchParams(router.query)

  const query = useQuery({ queryKey: queryKeys.followers(params), queryFn: () => toQuery(getFollower(params)), enabled: router.isReady, placeholderData: keepPreviousData })
  const queries = { datas: query }

  return (
    <QueryCheck title="Follower" queries={queries}>
      {(props) => <Followers {...props} />}
    </QueryCheck>
  )
}
