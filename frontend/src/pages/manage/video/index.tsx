import { useQuery } from '@tanstack/react-query'
import { channelsQuery, manageVideosQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageVideos from 'components/templates/manage/video'

export default function ManageVideosPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)

  const channels = useQuery(channelsQuery())
  const channel = router.query.channel?.toString() || channels.data?.[0]?.ulid
  const params = { search, channel, limit, offset }

  const data = useQuery({ ...manageVideosQuery(params), enabled: channels.isSuccess })
  const queries = { channels, data }

  return (
    <QueryCheck title="Video" queries={queries}>
      {(props) => <ManageVideos key={`${channel}-${search}-${page}`} {...props} page={page} />}
    </QueryCheck>
  )
}
