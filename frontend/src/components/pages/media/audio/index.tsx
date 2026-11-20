import { useSuspenseQuery } from '@tanstack/react-query'
import { audiosQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import Audios from './view'

export default function AudiosPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }
  const { data } = useSuspenseQuery(audiosQuery(params))

  return <Audios data={data} page={page} />
}
