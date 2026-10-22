import { useQuery } from '@tanstack/react-query'
import { channelsQuery, manageComicsQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageComics from 'components/templates/manage/comic'

export default function ManageComicsPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)

  const channels = useQuery(channelsQuery())
  const channel = router.query.channel?.toString() || channels.data?.[0]?.ulid
  const params = { search, channel, limit, offset }

  const data = useQuery({ ...manageComicsQuery(params), enabled: channels.isSuccess })
  const queries = { channels, data }

  return (
    <QueryCheck title="Comic" queries={queries}>
      {(props) => <ManageComics {...props} page={page} />}
    </QueryCheck>
  )
}
