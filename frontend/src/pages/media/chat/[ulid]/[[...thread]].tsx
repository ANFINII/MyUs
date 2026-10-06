import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getChat } from 'api/internal/media/detail'
import { useAppRouter } from 'components/hooks/useAppRouter'
import Custom404 from 'components/widgets/Status/Custom404'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ChatDetail from 'components/templates/media/chat/detail'

const parseThread = (thread: string | string[] | undefined): { isValid: boolean; threadUlid?: string } => {
  if (thread === undefined) return { isValid: true }
  if (Array.isArray(thread) && thread.length === 2 && thread[0] === 'thread') return { isValid: true, threadUlid: thread[1] }
  return { isValid: false }
}

export default function ChatDetailPage(): React.JSX.Element {
  const router = useAppRouter()
  const ulid = String(router.query.ulid ?? '')
  const { isValid, threadUlid } = parseThread(router.query.thread)

  const data = useQuery({ queryKey: queryKeys.mediaChatDetail(ulid), queryFn: () => toQuery(getChat(ulid)), enabled: router.isReady && isValid })
  const queries = { data }

  if (router.isReady && !isValid) return <Custom404 />

  return (
    <QueryCheck title="Chat" queries={queries} fresh>
      {(props) => <ChatDetail key={ulid} {...props} threadUlid={threadUlid} />}
    </QueryCheck>
  )
}
