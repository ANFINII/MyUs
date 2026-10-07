import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { useSearch } from '@tanstack/react-router'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getChannels } from 'api/internal/channel'
import { getManageBlogs } from 'api/internal/manage/get'
import { pageParams } from 'utils/functions/common'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageBlogs from 'components/templates/manage/blog'

export default function ManageBlogsPage(): React.JSX.Element {
  const query = useSearch({ strict: false })
  const { search, page, limit, offset } = pageParams(query)

  const channels = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })

  const channel = query.channel || channels.data?.[0]?.ulid
  const params = { search, channel, limit, offset }

  const data = useQuery({
    queryKey: queryKeys.manageBlogList(params),
    queryFn: () => toQuery(getManageBlogs(params)),
    enabled: channels.isSuccess,
    placeholderData: keepPreviousData,
  })
  const queries = { channels, data }

  return (
    <QueryCheck title="Blog" queries={queries}>
      {(props) => <ManageBlogs {...props} page={page} />}
    </QueryCheck>
  )
}
