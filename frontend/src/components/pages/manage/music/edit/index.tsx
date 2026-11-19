import { useSuspenseQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery, manageMusicQuery, paymentSellerQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import ManageMusicEdit from './view'

export default function ManageMusicEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const { data: channels } = useSuspenseQuery(channelsQuery())
  const { data: categories } = useSuspenseQuery(categoriesQuery())
  const { data } = useSuspenseQuery(manageMusicQuery(ulid))
  const { data: seller } = useSuspenseQuery(paymentSellerQuery())

  return <ManageMusicEdit channels={channels} categories={categories} data={data} seller={seller} />
}
