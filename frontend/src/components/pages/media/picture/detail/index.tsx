import { useSuspenseQuery } from '@tanstack/react-query'
import { pictureQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import PictureDetail from './view'

export default function PictureDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const { data } = useSuspenseQuery(pictureQuery(ulid))

  return <PictureDetail data={data} />
}
