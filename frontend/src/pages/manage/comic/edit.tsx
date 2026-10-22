import { useQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery, manageComicDetailQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageComicEdit from 'components/templates/manage/comic/edit'

export default function ManageComicEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const channels = useQuery(channelsQuery())
  const categories = useQuery(categoriesQuery())
  const data = useQuery(manageComicDetailQuery(ulid))
  const queries = { data, channels, categories }

  return (
    <QueryCheck title="Comic" queries={queries}>
      {(props) => <ManageComicEdit {...props} />}
    </QueryCheck>
  )
}
