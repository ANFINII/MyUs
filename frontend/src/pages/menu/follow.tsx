import { useQuery } from '@tanstack/react-query'
import { followsQuery } from 'lib/query/options'
import { searchParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Follows from 'components/templates/menu/follow'

export default function FollowsPage(): React.JSX.Element {
  const router = useRouter()
  const params = searchParams(router.query)
  const data = useQuery(followsQuery(params))
  const queries = { data }

  return (
    <QueryCheck title="Follow" queries={queries}>
      {(props) => <Follows {...props} />}
    </QueryCheck>
  )
}
