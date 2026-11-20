import { useSuspenseQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery, manageAudioQuery, paymentSellerQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import ManageAudioEdit from './view'

export default function ManageAudioEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const { data: channels } = useSuspenseQuery(channelsQuery())
  const { data: categories } = useSuspenseQuery(categoriesQuery())
  const { data: seller } = useSuspenseQuery(paymentSellerQuery())
  const { data } = useSuspenseQuery(manageAudioQuery(ulid))

  return <ManageAudioEdit channels={channels} categories={categories} seller={seller} data={data} />
}
