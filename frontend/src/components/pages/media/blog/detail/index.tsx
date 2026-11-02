import { useSuspenseQuery } from '@tanstack/react-query'
import { blogQuery } from 'lib/query/options'
import { useRouter } from 'components/hooks/useRouter'
import BlogDetail from './view'

export default function BlogDetailPage(): React.JSX.Element {
  const router = useRouter()
  const ulid = String(router.query.ulid ?? '')
  const { data } = useSuspenseQuery(blogQuery(ulid))

  return <BlogDetail data={data} />
}
