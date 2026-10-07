import { useQuery } from '@tanstack/react-query'
import { useParams } from '@tanstack/react-router'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getPicture } from 'api/internal/media/detail'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import PictureDetail from 'components/templates/media/picture/detail'

export default function PictureDetailPage(): React.JSX.Element {
  const { ulid } = useParams({ from: '/media/picture/$ulid' })

  const data = useQuery({ queryKey: queryKeys.mediaPictureDetail(ulid), queryFn: () => toQuery(getPicture(ulid)) })
  const queries = { data }

  return (
    <QueryCheck title="Picture" queries={queries} fresh>
      {(props) => <PictureDetail {...props} />}
    </QueryCheck>
  )
}
