import { useSuspenseQuery } from '@tanstack/react-query'
import { comicQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import ComicDetail from './view'

export default function ComicDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')
  const { data } = useSuspenseQuery(comicQuery(ulid))

  return <ComicDetail data={data} />
}
