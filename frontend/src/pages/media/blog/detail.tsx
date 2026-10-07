import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getBlog } from 'api/internal/media/detail'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import BlogDetail from 'components/templates/media/blog/detail'

export default function BlogDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery({ queryKey: queryKeys.mediaBlogDetail(ulid), queryFn: () => toQuery(getBlog(ulid)) })
  const queries = { data }

  return (
    <QueryCheck title="Blog" queries={queries} fresh>
      {(props) => <BlogDetail {...props} />}
    </QueryCheck>
  )
}
