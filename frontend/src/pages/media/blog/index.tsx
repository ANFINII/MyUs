import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getBlogs } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Blogs from 'components/templates/media/blog/list'

export default function BlogsPage(): React.JSX.Element {
  const router = useAppRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }

  const data = useQuery({ queryKey: queryKeys.mediaBlogList(params), queryFn: () => toQuery(getBlogs(params)), enabled: router.isReady, placeholderData: keepPreviousData })
  const queries = { data }

  return (
    <QueryCheck title="Blog" queries={queries}>
      {(props) => <Blogs {...props} page={page} />}
    </QueryCheck>
  )
}
