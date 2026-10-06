import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getChats } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Chats from 'components/templates/media/chat/list'

export default function ChatsPage(): React.JSX.Element {
  const router = useAppRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }

  const query = useQuery({ queryKey: queryKeys.mediaChatList(params), queryFn: () => toQuery(getChats(params)), enabled: router.isReady, placeholderData: keepPreviousData })
  const queries = { list: query }

  return (
    <QueryCheck title="Chat" queries={queries}>
      {(props) => <Chats {...props} page={page} />}
    </QueryCheck>
  )
}
