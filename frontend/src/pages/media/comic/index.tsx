import { useQuery } from '@tanstack/react-query'
import { comicListQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Comics from 'components/templates/media/comic/list'

export default function ComicsPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }

  const data = useQuery(comicListQuery(params))
  const queries = { data }

  return (
    <QueryCheck title="Comic" queries={queries}>
      {(props) => <Comics {...props} page={page} />}
    </QueryCheck>
  )
}
