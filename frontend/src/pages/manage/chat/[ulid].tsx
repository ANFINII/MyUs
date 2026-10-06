import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import { getManageChat } from 'api/internal/manage/get'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageChatEdit from 'components/templates/manage/chat/edit'

export default function ManageChatEditPage(): React.JSX.Element {
  const router = useAppRouter()
  const ulid = String(router.query.ulid ?? '')

  const channels = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })
  const categories = useQuery({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()) })
  const data = useQuery({ queryKey: queryKeys.manageChatDetail(ulid), queryFn: () => toQuery(getManageChat(ulid)), enabled: router.isReady })
  const queries = { data, channels, categories }

  return (
    <QueryCheck title="Chat" queries={queries} fresh>
      {(props) => <ManageChatEdit {...props} />}
    </QueryCheck>
  )
}
