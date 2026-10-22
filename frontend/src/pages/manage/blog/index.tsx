import { useQuery } from '@tanstack/react-query'
import { channelsQuery, manageBlogsQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageBlogs from 'components/templates/manage/blog'

export default function ManageBlogsPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)

  const channels = useQuery(channelsQuery())
  const channel = router.query.channel?.toString() || channels.data?.[0]?.ulid
  const params = { search, channel, limit, offset }

  const data = useQuery({ ...manageBlogsQuery(params), enabled: channels.isSuccess })
  const queries = { channels, data }

  return (
    <QueryCheck title="Blog" queries={queries}>
      {(props) => <ManageBlogs {...props} page={page} />}
    </QueryCheck>
  )
}
