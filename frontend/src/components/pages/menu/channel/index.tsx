import { useSuspenseQuery } from '@tanstack/react-query'
import { subscribeChannelsQuery } from 'lib/query/options'
import Channels from './view'

export default function ChannelsPage(): React.JSX.Element {
  const { data } = useSuspenseQuery(subscribeChannelsQuery())

  return <Channels data={data} />
}
