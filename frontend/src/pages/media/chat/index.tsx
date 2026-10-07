import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { useSearch } from '@tanstack/react-router'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getChats } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Chats from 'components/templates/media/chat/list'

export default function ChatsPage(): React.JSX.Element {
  const query = useSearch({ strict: false })
  const { search, page, limit, offset } = pageParams(query)
  const params = { search, limit, offset }

  const data = useQuery({ queryKey: queryKeys.mediaChatList(params), queryFn: () => toQuery(getChats(params)), placeholderData: keepPreviousData })
  const queries = { data }

  return (
    <QueryCheck title="Chat" queries={queries}>
      {(props) => <Chats {...props} page={page} />}
    </QueryCheck>
  )
}
