import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { useSearch } from '@tanstack/react-router'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getChannels } from 'api/internal/channel'
import { getManageMusics } from 'api/internal/manage/get'
import { pageParams } from 'utils/functions/common'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageMusics from 'components/templates/manage/music'

export default function ManageMusicsPage(): React.JSX.Element {
  const query = useSearch({ strict: false })
  const { search, page, limit, offset } = pageParams(query)

  const channels = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })

  const channel = query.channel || channels.data?.[0]?.ulid
  const params = { search, channel, limit, offset }

  const data = useQuery({
    queryKey: queryKeys.manageMusicList(params),
    queryFn: () => toQuery(getManageMusics(params)),
    enabled: channels.isSuccess,
    placeholderData: keepPreviousData,
  })
  const queries = { channels, data }

  return (
    <QueryCheck title="Music" queries={queries}>
      {(props) => <ManageMusics {...props} page={page} />}
    </QueryCheck>
  )
}
