import { useSuspenseQuery } from '@tanstack/react-query'
import { chatsQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import Chats from './view'

export default function ChatsPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }
  const { data } = useSuspenseQuery(chatsQuery(params))

  return <Chats data={data} page={page} />
}
