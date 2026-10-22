import { useQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery, manageVideoQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageVideoEdit from 'components/templates/manage/video/edit'

export default function ManageVideoEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const channels = useQuery(channelsQuery())
  const categories = useQuery(categoriesQuery())
  const data = useQuery(manageVideoQuery(ulid))
  const queries = { data, channels, categories }

  return (
    <QueryCheck title="Video" queries={queries}>
      {(props) => <ManageVideoEdit {...props} />}
    </QueryCheck>
  )
}
