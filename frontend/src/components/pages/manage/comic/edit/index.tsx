import { useSuspenseQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery, manageComicQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import ManageComicEdit from './view'

export default function ManageComicEditPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')

  const { data: channels } = useSuspenseQuery(channelsQuery())
  const { data: categories } = useSuspenseQuery(categoriesQuery())
  const { data } = useSuspenseQuery(manageComicQuery(ulid))

  return <ManageComicEdit data={data} channels={channels} categories={categories} />
}
