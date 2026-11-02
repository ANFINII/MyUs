import { useSuspenseQuery } from '@tanstack/react-query'
import { channelsQuery, manageMusicsQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import ManageMusics from './view'

export default function ManageMusicsPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)

  const { data: channels } = useSuspenseQuery(channelsQuery())
  const channel = String(router.query.channel ?? '') || channels[0]?.ulid
  const params = { search, channel, limit, offset }

  const { data } = useSuspenseQuery(manageMusicsQuery(params))

  return <ManageMusics key={`${channel}-${search}-${page}`} channels={channels} data={data} page={page} />
}
