import { useSuspenseQuery } from '@tanstack/react-query'
import { channelsQuery, manageSeriesListQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import ManageSeriesList from './view'

export default function ManageSeriesListPage(): React.JSX.Element {
  const router = useRouter()

  const { data: channels } = useSuspenseQuery(channelsQuery())
  const channel = String(router.query.channel ?? '') || channels[0]?.ulid || ''
  const { data } = useSuspenseQuery(manageSeriesListQuery(channel))

  return <ManageSeriesList key={channel} channels={channels} data={data} channel={channel} />
}
