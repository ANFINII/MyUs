import { useQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery, manageBlogQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageBlogEdit from 'components/templates/manage/blog/edit'

export default function ManageBlogEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const channels = useQuery(channelsQuery())
  const categories = useQuery(categoriesQuery())
  const data = useQuery(manageBlogQuery(ulid))
  const queries = { data, channels, categories }

  return (
    <QueryCheck title="Blog" queries={queries}>
      {(props) => <ManageBlogEdit {...props} />}
    </QueryCheck>
  )
}
