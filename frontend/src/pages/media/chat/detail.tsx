import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { ChatDetailOut } from 'types/internal/media/output'
import { getChat } from 'api/internal/media/detail'
import { postMediaRead } from 'api/internal/media/read'
import { MediaType } from 'utils/constants/enum'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ChatDetail from 'components/templates/media/chat/detail'

const getDetail = async (ulid: string): Promise<ChatDetailOut> => {
  await postMediaRead({ ulid, mediaType: MediaType.Chat })
  return await toQuery(getChat(ulid))
}

export default function ChatDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')
  const threadUlid = router.query.messageUlid?.toString()

  const data = useQuery({ queryKey: queryKeys.mediaChatDetail(ulid), queryFn: () => getDetail(ulid) })
  const queries = { data }

  return (
    <QueryCheck title="Chat" queries={queries} fresh>
      {(props) => <ChatDetail key={ulid} {...props} threadUlid={threadUlid} />}
    </QueryCheck>
  )
}
