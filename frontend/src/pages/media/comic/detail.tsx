import { useQuery } from '@tanstack/react-query'
import { useParams } from '@tanstack/react-router'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getComic } from 'api/internal/media/detail'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ComicDetail from 'components/templates/media/comic/detail'

export default function ComicDetailPage(): React.JSX.Element {
  const { ulid } = useParams({ from: '/media/comic/$ulid' })

  const data = useQuery({ queryKey: queryKeys.mediaComicDetail(ulid), queryFn: () => toQuery(getComic(ulid)) })
  const queries = { data }

  return (
    <QueryCheck title="Comic" queries={queries} fresh>
      {(props) => <ComicDetail {...props} />}
    </QueryCheck>
  )
}
