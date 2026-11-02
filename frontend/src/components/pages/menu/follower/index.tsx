import { useSuspenseQuery } from '@tanstack/react-query'
import { followersQuery } from 'lib/query/options'
import { searchParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import Followers from './view'

export default function FollowersPage(): React.JSX.Element {
  const router = useRouter()
  const params = searchParams(router.query)
  const { data } = useSuspenseQuery(followersQuery(params))

  return <Followers data={data} />
}
