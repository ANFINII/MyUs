import { useQuery } from '@tanstack/react-query'
import { useParams } from '@tanstack/react-router'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import { getManageMusic } from 'api/internal/manage/get'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageMusicEdit from 'components/templates/manage/music/edit'

export default function ManageMusicEditPage(): React.JSX.Element {
  const { ulid } = useParams({ from: '/manage/music/$ulid' })

  const channels = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })
  const categories = useQuery({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()) })
  const data = useQuery({ queryKey: queryKeys.manageMusicDetail(ulid), queryFn: () => toQuery(getManageMusic(ulid)) })
  const queries = { data, channels, categories }

  return (
    <QueryCheck title="Music" queries={queries} fresh>
      {(props) => <ManageMusicEdit {...props} />}
    </QueryCheck>
  )
}
