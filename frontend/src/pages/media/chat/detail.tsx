import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getChat } from 'api/internal/media/detail'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ChatDetail from 'components/templates/media/chat/detail'

export default function ChatDetailPage(): React.JSX.Element {
  const router = useAppRouter()
  const ulid = String(router.query.ulid ?? '')
  const threadUlid = router.query.messageUlid?.toString()

  const data = useQuery({ queryKey: queryKeys.mediaChatDetail(ulid), queryFn: () => toQuery(getChat(ulid)) })
  const queries = { data }

  return (
    <QueryCheck title="Chat" queries={queries} fresh>
      {(props) => <ChatDetail key={ulid} {...props} threadUlid={threadUlid} />}
    </QueryCheck>
  )
}
