import { useSuspenseQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery, manageChatQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import ManageChatEdit from './view'

export default function ManageChatEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const { data: channels } = useSuspenseQuery(channelsQuery())
  const { data: categories } = useSuspenseQuery(categoriesQuery())
  const { data } = useSuspenseQuery(manageChatQuery(ulid))

  return <ManageChatEdit data={data} channels={channels} categories={categories} />
}
