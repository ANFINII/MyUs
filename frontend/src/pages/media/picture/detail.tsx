import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getPicture } from 'api/internal/media/detail'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import PictureDetail from 'components/templates/media/picture/detail'

export default function PictureDetailPage(): React.JSX.Element {
  const router = useAppRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery({ queryKey: queryKeys.mediaPictureDetail(ulid), queryFn: () => toQuery(getPicture(ulid)) })
  const queries = { data }

  return (
    <QueryCheck title="Picture" queries={queries} fresh>
      {(props) => <PictureDetail {...props} />}
    </QueryCheck>
  )
}
