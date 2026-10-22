import { useQuery } from '@tanstack/react-query'
import { chatQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ChatDetail from 'components/templates/media/chat/detail'

export default function ChatDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')
  const threadUlid = String(router.query.messageUlid ?? '')

  const data = useQuery(chatQuery(ulid))
  const queries = { data }

  return (
    <QueryCheck title="Chat" queries={queries}>
      {(props) => <ChatDetail key={ulid} {...props} threadUlid={threadUlid} />}
    </QueryCheck>
  )
}
