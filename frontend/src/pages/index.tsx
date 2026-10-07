import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { useSearch } from '@tanstack/react-router'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getHome } from 'api/internal/media/list'
import { searchParams } from 'utils/functions/common'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Homes from 'components/templates/media/home/list'

export default function HomesPage(): React.JSX.Element {
  const query = useSearch({ strict: false })
  const params = searchParams(query)

  const mediaHome = useQuery({ queryKey: queryKeys.home(params), queryFn: () => toQuery(getHome(params)), placeholderData: keepPreviousData })
  const queries = { mediaHome }

  return (
    <QueryCheck title="Home" queries={queries}>
      {(props) => <Homes title="Home" {...props} />}
    </QueryCheck>
  )
}
