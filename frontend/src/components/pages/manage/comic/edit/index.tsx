import { useSuspenseQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery, manageComicQuery, paymentSellerQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import ManageComicEdit from './view'

export default function ManageComicEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const { data: channels } = useSuspenseQuery(channelsQuery())
  const { data: categories } = useSuspenseQuery(categoriesQuery())
  const { data } = useSuspenseQuery(manageComicQuery(ulid))
  const { data: seller } = useSuspenseQuery(paymentSellerQuery())

  return <ManageComicEdit channels={channels} categories={categories} data={data} seller={seller} />
}
