import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getComic } from 'api/internal/media/detail'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ComicDetail from 'components/templates/media/comic/detail'

export default function ComicDetailPage(): React.JSX.Element {
  const router = useAppRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery({ queryKey: queryKeys.mediaComicDetail(ulid), queryFn: () => toQuery(getComic(ulid)) })
  const queries = { data }

  return (
    <QueryCheck title="Comic" queries={queries} fresh>
      {(props) => <ComicDetail {...props} />}
    </QueryCheck>
  )
}
