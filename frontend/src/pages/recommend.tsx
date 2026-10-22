import { useQuery } from '@tanstack/react-query'
import { recommendQuery } from 'lib/query/options'
import { searchParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Homes from 'components/templates/media/home/list'

export default function RecommendPage(): React.JSX.Element {
  const router = useRouter()
  const params = searchParams(router.query)
  const data = useQuery(recommendQuery(params))
  const queries = { data }

  return (
    <QueryCheck title="Recommend" queries={queries}>
      {(props) => <Homes title="Recommend" {...props} />}
    </QueryCheck>
  )
}
