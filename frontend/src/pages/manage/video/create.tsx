import { useQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery } from 'lib/query/options'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import VideoCreate from 'components/templates/manage/video/create'

export default function VideoCreatePage(): React.JSX.Element {
  const channels = useQuery(channelsQuery())
  const categories = useQuery(categoriesQuery())
  const queries = { channels, categories }

  return (
    <QueryCheck title="Video" queries={queries}>
      {(props) => <VideoCreate {...props} />}
    </QueryCheck>
  )
}
