import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getHome } from 'api/internal/media/list'
import { searchParams } from 'utils/functions/common'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Homes from 'components/templates/media/home/list'

export default function HomesPage(): React.JSX.Element {
  const router = useAppRouter()
  const params = searchParams(router.query)

  const query = useQuery({ queryKey: queryKeys.home(params), queryFn: () => toQuery(getHome(params)), enabled: router.isReady, placeholderData: keepPreviousData })
  const queries = { mediaHome: query }

  return (
    <QueryCheck title="Home" queries={queries}>
      {(props) => <Homes title="Home" {...props} />}
    </QueryCheck>
  )
}
