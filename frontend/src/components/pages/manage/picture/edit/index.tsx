import { useSuspenseQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery, managePictureQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import ManagePictureEdit from './view'

export default function ManagePictureEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const { data: channels } = useSuspenseQuery(channelsQuery())
  const { data: categories } = useSuspenseQuery(categoriesQuery())
  const { data } = useSuspenseQuery(managePictureQuery(ulid))

  return <ManagePictureEdit channels={channels} categories={categories} data={data} />
}
