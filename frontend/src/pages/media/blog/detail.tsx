import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getBlog } from 'api/internal/media/detail'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import BlogDetail from 'components/templates/media/blog/detail'

export default function BlogDetailPage(): React.JSX.Element {
  const router = useAppRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery({ queryKey: queryKeys.mediaBlogDetail(ulid), queryFn: () => toQuery(getBlog(ulid)), enabled: router.isReady })
  const queries = { data }

  return (
    <QueryCheck title="Blog" queries={queries} fresh>
      {(props) => <BlogDetail {...props} />}
    </QueryCheck>
  )
}
