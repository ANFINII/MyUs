import { useSuspenseQuery } from '@tanstack/react-query'
import { musicsQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import Musics from './view'

export default function MusicsPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }

  const { data } = useSuspenseQuery(musicsQuery(params))

  return <Musics data={data} page={page} />
}
