import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import { getManageVideo } from 'api/internal/manage/get'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageVideoEdit from 'components/templates/manage/video/edit'

export default function ManageVideoEditPage(): React.JSX.Element {
  const router = useAppRouter()
  const ulid = String(router.query.ulid ?? '')

  const channelsQuery = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })
  const categoriesQuery = useQuery({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()) })
  const query = useQuery({ queryKey: queryKeys.manageVideoDetail(ulid), queryFn: () => toQuery(getManageVideo(ulid)), enabled: router.isReady })
  const queries = { data: query, channels: channelsQuery, categories: categoriesQuery }

  return (
    <QueryCheck title="Video" queries={queries} fresh>
      {(props) => <ManageVideoEdit {...props} />}
    </QueryCheck>
  )
}
