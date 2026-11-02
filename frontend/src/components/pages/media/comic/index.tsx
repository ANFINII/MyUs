import { useSuspenseQuery } from '@tanstack/react-query'
import { comicsQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import Comics from './view'

export default function ComicsPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }

  const { data } = useSuspenseQuery(comicsQuery(params))

  return <Comics data={data} page={page} />
}
