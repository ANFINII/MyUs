import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { PictureDetailOut } from 'types/internal/media/output'
import { getPicture, postMediaRead } from 'api/internal/media/detail'
import { MediaType } from 'utils/constants/enum'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import PictureDetail from 'components/templates/media/picture/detail'

const getDetail = async (ulid: string): Promise<PictureDetailOut> => {
  await postMediaRead({ ulid, mediaType: MediaType.Picture })
  return await toQuery(getPicture(ulid))
}

export default function PictureDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery({ queryKey: queryKeys.mediaPictureDetail(ulid), queryFn: () => getDetail(ulid) })
  const queries = { data }

  return (
    <QueryCheck title="Picture" queries={queries} fresh>
      {(props) => <PictureDetail {...props} />}
    </QueryCheck>
  )
}
