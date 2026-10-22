import { useQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery, managePictureDetailQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManagePictureEdit from 'components/templates/manage/picture/edit'

export default function ManagePictureEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const channels = useQuery(channelsQuery())
  const categories = useQuery(categoriesQuery())
  const data = useQuery(managePictureDetailQuery(ulid))
  const queries = { data, channels, categories }

  return (
    <QueryCheck title="Picture" queries={queries}>
      {(props) => <ManagePictureEdit {...props} />}
    </QueryCheck>
  )
}
