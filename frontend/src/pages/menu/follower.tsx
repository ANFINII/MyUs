import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { useSearch } from '@tanstack/react-router'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getFollower } from 'api/internal/user'
import { searchParams } from 'utils/functions/common'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Followers from 'components/templates/menu/follower'

export default function FollowersPage(): React.JSX.Element {
  const query = useSearch({ strict: false })
  const params = searchParams(query)

  const datas = useQuery({ queryKey: queryKeys.followers(params), queryFn: () => toQuery(getFollower(params)), placeholderData: keepPreviousData })
  const queries = { datas }

  return (
    <QueryCheck title="Follower" queries={queries}>
      {(props) => <Followers {...props} />}
    </QueryCheck>
  )
}
