import { useSuspenseQuery } from '@tanstack/react-query'
import { videosQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import Videos from './view'

export default function VideosPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }
  const { data } = useSuspenseQuery(videosQuery(params))

  return <Videos data={data} page={page} />
}
