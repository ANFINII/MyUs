import { useQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery, manageMusicQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageMusicEdit from 'components/templates/manage/music/edit'

export default function ManageMusicEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const channels = useQuery(channelsQuery())
  const categories = useQuery(categoriesQuery())
  const data = useQuery(manageMusicQuery(ulid))
  const queries = { data, channels, categories }

  return (
    <QueryCheck title="Music" queries={queries}>
      {(props) => <ManageMusicEdit {...props} />}
    </QueryCheck>
  )
}
