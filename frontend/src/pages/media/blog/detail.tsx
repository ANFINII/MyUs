import { useQuery } from '@tanstack/react-query'
import { blogDetailQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import BlogDetail from 'components/templates/media/blog/detail'

export default function BlogDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery(blogDetailQuery(ulid))
  const queries = { data }

  return (
    <QueryCheck title="Blog" queries={queries}>
      {(props) => <BlogDetail {...props} />}
    </QueryCheck>
  )
}
