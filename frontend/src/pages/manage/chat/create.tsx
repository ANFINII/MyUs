import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ChatCreate from 'components/templates/manage/chat/create'

export default function ChatCreatePage(): React.JSX.Element {
  const channels = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })
  const categories = useQuery({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()) })
  const queries = { channels, categories }

  return (
    <QueryCheck title="Chat" queries={queries} fresh>
      {(props) => <ChatCreate {...props} />}
    </QueryCheck>
  )
}
