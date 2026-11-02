import { useSuspenseQuery } from '@tanstack/react-query'
import { channelsQuery, manageBlogsQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import ManageBlogs from './view'

export default function ManageBlogsPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)

  const { data: channels } = useSuspenseQuery(channelsQuery())
  const channel = router.query.channel?.toString() || channels[0]?.ulid
  const params = { search, channel, limit, offset }

  const { data } = useSuspenseQuery(manageBlogsQuery(params))

  return <ManageBlogs key={`${channel}-${search}-${page}`} channels={channels} data={data} page={page} />
}
