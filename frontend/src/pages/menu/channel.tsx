import { useQuery } from '@tanstack/react-query'
import { subscribeChannelsQuery } from 'lib/query/options'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Channels from 'components/templates/menu/channel'

export default function ChannelsPage(): React.JSX.Element {
  const data = useQuery(subscribeChannelsQuery())
  const queries = { data }

  return (
    <QueryCheck title="Channel" queries={queries}>
      {(props) => <Channels {...props} />}
    </QueryCheck>
  )
}
