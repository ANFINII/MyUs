import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import VideoCreate from 'components/templates/manage/video/create'

export default function VideoCreatePage(): React.JSX.Element {
  const channels = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })
  const categories = useQuery({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()) })
  const queries = { channels, categories }

  return (
    <QueryCheck title="Video" queries={queries} fresh>
      {(props) => <VideoCreate {...props} />}
    </QueryCheck>
  )
}
