import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { homeQuery } from 'lib/query/options'
import { searchParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Homes from 'components/templates/media/home/list'

export default function HomesPage(): React.JSX.Element {
  const router = useRouter()
  const params = searchParams(router.query)
  const data = useQuery({ ...homeQuery(params), placeholderData: keepPreviousData, refetchOnMount: false })
  const queries = { data }

  return (
    <QueryCheck title="Home" queries={queries}>
      {(props) => <Homes title="Home" {...props} />}
    </QueryCheck>
  )
}
