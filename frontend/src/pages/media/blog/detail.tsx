import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { BlogDetailOut } from 'types/internal/media/output'
import { getBlog } from 'api/internal/media/detail'
import { postMediaRead } from 'api/internal/media/read'
import { MediaType } from 'utils/constants/enum'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import BlogDetail from 'components/templates/media/blog/detail'

const getDetail = async (ulid: string): Promise<BlogDetailOut> => {
  await postMediaRead({ ulid, mediaType: MediaType.Blog })
  return await toQuery(getBlog(ulid))
}

export default function BlogDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery({ queryKey: queryKeys.mediaBlogDetail(ulid), queryFn: () => getDetail(ulid) })
  const queries = { data }

  return (
    <QueryCheck title="Blog" queries={queries} fresh>
      {(props) => <BlogDetail {...props} />}
    </QueryCheck>
  )
}
