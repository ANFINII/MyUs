import { useSuspenseQuery } from '@tanstack/react-query'
import { picturesQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import Pictures from './view'

export default function PicturesPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }
  const { data } = useSuspenseQuery(picturesQuery(params))

  return <Pictures data={data} page={page} />
}
