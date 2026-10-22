import { useQuery } from '@tanstack/react-query'
import { followersQuery } from 'lib/query/options'
import { searchParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Followers from 'components/templates/menu/follower'

export default function FollowersPage(): React.JSX.Element {
  const router = useRouter()
  const params = searchParams(router.query)
  const data = useQuery(followersQuery(params))
  const queries = { data }

  return (
    <QueryCheck title="Follower" queries={queries}>
      {(props) => <Followers {...props} />}
    </QueryCheck>
  )
}
