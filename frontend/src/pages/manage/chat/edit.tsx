import { useQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery, manageChatDetailQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageChatEdit from 'components/templates/manage/chat/edit'

export default function ManageChatEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const channels = useQuery(channelsQuery())
  const categories = useQuery(categoriesQuery())
  const data = useQuery(manageChatDetailQuery(ulid))
  const queries = { data, channels, categories }

  return (
    <QueryCheck title="Chat" queries={queries}>
      {(props) => <ManageChatEdit {...props} />}
    </QueryCheck>
  )
}
