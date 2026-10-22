import { useQuery } from '@tanstack/react-query'
import { comicDetailQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ComicDetail from 'components/templates/media/comic/detail'

export default function ComicDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery(comicDetailQuery(ulid))
  const queries = { data }

  return (
    <QueryCheck title="Comic" queries={queries}>
      {(props) => <ComicDetail {...props} />}
    </QueryCheck>
  )
}
