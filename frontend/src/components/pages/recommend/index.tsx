import { useSuspenseQuery } from '@tanstack/react-query'
import { recommendQuery } from 'lib/query/options'
import { searchParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import Homes from 'components/pages/home/view'

export default function RecommendPage(): React.JSX.Element {
  const router = useRouter()
  const params = searchParams(router.query)
  const { data } = useSuspenseQuery(recommendQuery(params))

  return <Homes title="Recommend" data={data} />
}
