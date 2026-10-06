import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import { getManageMusic } from 'api/internal/manage/get'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageMusicEdit from 'components/templates/manage/music/edit'

export default function ManageMusicEditPage(): React.JSX.Element {
  const router = useAppRouter()
  const ulid = String(router.query.ulid ?? '')

  const channelsQuery = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })
  const categoriesQuery = useQuery({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()) })
  const query = useQuery({ queryKey: queryKeys.manageMusicDetail(ulid), queryFn: () => toQuery(getManageMusic(ulid)), enabled: router.isReady })
  const queries = { data: query, channels: channelsQuery, categories: categoriesQuery }

  return (
    <QueryCheck title="Music" queries={queries} fresh>
      {(props) => <ManageMusicEdit {...props} />}
    </QueryCheck>
  )
}
