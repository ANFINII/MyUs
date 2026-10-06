import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getRecommend } from 'api/internal/media/list'
import { searchParams } from 'utils/functions/common'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Homes from 'components/templates/media/home/list'

export default function RecommendPage(): React.JSX.Element {
  const router = useAppRouter()
  const params = searchParams(router.query)

  const mediaHome = useQuery({ queryKey: queryKeys.recommend(params), queryFn: () => toQuery(getRecommend(params)), enabled: router.isReady, placeholderData: keepPreviousData })
  const queries = { mediaHome }

  return (
    <QueryCheck title="Recommend" queries={queries}>
      {(props) => <Homes title="Recommend" {...props} />}
    </QueryCheck>
  )
}
