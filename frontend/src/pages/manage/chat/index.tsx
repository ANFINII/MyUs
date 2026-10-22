import { useQuery } from '@tanstack/react-query'
import { channelsQuery, manageChatsQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageChats from 'components/templates/manage/chat'

export default function ManageChatsPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)

  const channels = useQuery(channelsQuery())
  const channel = router.query.channel?.toString() || channels.data?.[0]?.ulid
  const params = { search, channel, limit, offset }

  const data = useQuery({ ...manageChatsQuery(params), enabled: channels.isSuccess })
  const queries = { channels, data }

  return (
    <QueryCheck title="Chat" queries={queries}>
      {(props) => <ManageChats {...props} page={page} />}
    </QueryCheck>
  )
}
