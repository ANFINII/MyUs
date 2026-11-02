import { useSuspenseQuery } from '@tanstack/react-query'
import { chatQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import ChatDetail from './view'

export default function ChatDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')
  const threadUlid = String(router.query.messageUlid ?? '')

  const { data } = useSuspenseQuery(chatQuery(ulid))

  return <ChatDetail key={ulid} data={data} threadUlid={threadUlid} />
}
