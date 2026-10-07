import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import { getManageVideo } from 'api/internal/manage/get'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageVideoEdit from 'components/templates/manage/video/edit'

export default function ManageVideoEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const channels = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })
  const categories = useQuery({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()) })
  const data = useQuery({ queryKey: queryKeys.manageVideoDetail(ulid), queryFn: () => toQuery(getManageVideo(ulid)) })
  const queries = { data, channels, categories }

  return (
    <QueryCheck title="Video" queries={queries} fresh>
      {(props) => <ManageVideoEdit {...props} />}
    </QueryCheck>
  )
}
