import { useQuery } from '@tanstack/react-query'
import { pictureQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import PictureDetail from 'components/templates/media/picture/detail'

export default function PictureDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery(pictureQuery(ulid))
  const queries = { data }

  return (
    <QueryCheck title="Picture" queries={queries}>
      {(props) => <PictureDetail {...props} />}
    </QueryCheck>
  )
}
