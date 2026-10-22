import { useQuery } from '@tanstack/react-query'
import { chatListQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Chats from 'components/templates/media/chat/list'

export default function ChatsPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }

  const data = useQuery(chatListQuery(params))
  const queries = { data }

  return (
    <QueryCheck title="Chat" queries={queries}>
      {(props) => <Chats {...props} page={page} />}
    </QueryCheck>
  )
}
