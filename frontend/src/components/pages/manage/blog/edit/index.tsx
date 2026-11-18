import { useSuspenseQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery, manageBlogQuery, paymentSellerQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import ManageBlogEdit from './view'

export default function ManageBlogEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const { data: channels } = useSuspenseQuery(channelsQuery())
  const { data: categories } = useSuspenseQuery(categoriesQuery())
  const { data } = useSuspenseQuery(manageBlogQuery(ulid))
  const { data: seller } = useSuspenseQuery(paymentSellerQuery())

  return <ManageBlogEdit channels={channels} categories={categories} data={data} seller={seller} />
}
