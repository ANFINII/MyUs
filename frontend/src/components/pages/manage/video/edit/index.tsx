import { useSuspenseQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery, manageVideoQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import ManageVideoEdit from './view'

export default function ManageVideoEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const { data: channels } = useSuspenseQuery(channelsQuery())
  const { data: categories } = useSuspenseQuery(categoriesQuery())
  const { data } = useSuspenseQuery(manageVideoQuery(ulid))

  return <ManageVideoEdit data={data} channels={channels} categories={categories} />
}
