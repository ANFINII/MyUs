import { useQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery } from 'lib/query/options'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ChatCreate from 'components/templates/manage/chat/create'

export default function ChatCreatePage(): React.JSX.Element {
  const channels = useQuery(channelsQuery())
  const categories = useQuery(categoriesQuery())
  const queries = { channels, categories }

  return (
    <QueryCheck title="Chat" queries={queries}>
      {(props) => <ChatCreate {...props} />}
    </QueryCheck>
  )
}
