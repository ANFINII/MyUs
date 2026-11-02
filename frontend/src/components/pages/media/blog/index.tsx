import { useSuspenseQuery } from '@tanstack/react-query'
import { blogsQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import Blogs from './view'

export default function BlogsPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }

  const { data } = useSuspenseQuery(blogsQuery(params))

  return <Blogs data={data} page={page} />
}
