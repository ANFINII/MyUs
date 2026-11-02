import { useSuspenseQuery } from '@tanstack/react-query'
import { followsQuery } from 'lib/query/options'
import { searchParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import Follows from './view'

export default function FollowsPage(): React.JSX.Element {
  const router = useRouter()
  const params = searchParams(router.query)
  const { data } = useSuspenseQuery(followsQuery(params))

  return <Follows data={data} />
}
