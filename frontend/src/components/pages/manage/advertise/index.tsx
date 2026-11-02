import { useSuspenseQuery } from '@tanstack/react-query'
import { manageAdvertisesQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import ManageAdvertises from './view'

export default function ManageAdvertisesPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }
  const { data } = useSuspenseQuery(manageAdvertisesQuery(params))

  return <ManageAdvertises key={`${search}-${page}`} data={data} page={page} />
}
