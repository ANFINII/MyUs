import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { useSearch } from '@tanstack/react-router'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getBlogs } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Blogs from 'components/templates/media/blog/list'

export default function BlogsPage(): React.JSX.Element {
  const query = useSearch({ strict: false })
  const { search, page, limit, offset } = pageParams(query)
  const params = { search, limit, offset }

  const data = useQuery({ queryKey: queryKeys.mediaBlogList(params), queryFn: () => toQuery(getBlogs(params)), placeholderData: keepPreviousData })
  const queries = { data }

  return (
    <QueryCheck title="Blog" queries={queries}>
      {(props) => <Blogs {...props} page={page} />}
    </QueryCheck>
  )
}
