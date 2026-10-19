import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { ComicDetailOut } from 'types/internal/media/output'
import { getComic, postMediaRead } from 'api/internal/media/detail'
import { MediaType } from 'utils/constants/enum'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ComicDetail from 'components/templates/media/comic/detail'

const getDetail = async (ulid: string): Promise<ComicDetailOut> => {
  await postMediaRead({ ulid, mediaType: MediaType.Comic })
  return await toQuery(getComic(ulid))
}

export default function ComicDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const data = useQuery({ queryKey: queryKeys.mediaComicDetail(ulid), queryFn: () => getDetail(ulid) })
  const queries = { data }

  return (
    <QueryCheck title="Comic" queries={queries} fresh>
      {(props) => <ComicDetail {...props} />}
    </QueryCheck>
  )
}
