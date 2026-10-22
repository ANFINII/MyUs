import { useQuery } from '@tanstack/react-query'
import { channelsQuery, manageMusicListQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageMusics from 'components/templates/manage/music'

export default function ManageMusicsPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)

  const channels = useQuery(channelsQuery())
  const channel = router.query.channel?.toString() || channels.data?.[0]?.ulid
  const params = { search, channel, limit, offset }

  const data = useQuery({ ...manageMusicListQuery(params), enabled: channels.isSuccess })
  const queries = { channels, data }

  return (
    <QueryCheck title="Music" queries={queries}>
      {(props) => <ManageMusics {...props} page={page} />}
    </QueryCheck>
  )
}
