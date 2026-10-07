import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getComic } from 'api/internal/media/detail'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ComicDetail from 'components/templates/media/comic/detail'

export default function ComicDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery({ queryKey: queryKeys.mediaComicDetail(ulid), queryFn: () => toQuery(getComic(ulid)) })
  const queries = { data }

  return (
    <QueryCheck title="Comic" queries={queries} fresh>
      {(props) => <ComicDetail {...props} />}
    </QueryCheck>
  )
}
