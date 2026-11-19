import { useSuspenseQuery } from '@tanstack/react-query'
import { homeQuery } from 'lib/query/options'
import { homeParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import Homes from './view'

export default function HomesPage(): React.JSX.Element {
  const router = useRouter()
  const params = homeParams(router.query)
  const { data } = useSuspenseQuery(homeQuery(params))

  return <Homes title="Home" data={data} sort={params.sort} />
}
