import { useQuery } from '@tanstack/react-query'
import { blogListQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Blogs from 'components/templates/media/blog/list'

export default function BlogsPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }

  const data = useQuery(blogListQuery(params))
  const queries = { data }

  return (
    <QueryCheck title="Blog" queries={queries}>
      {(props) => <Blogs {...props} page={page} />}
    </QueryCheck>
  )
}
