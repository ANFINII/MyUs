import { useSuspenseQuery } from '@tanstack/react-query'
import { channelsQuery, manageComicsQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import ManageComics from './view'

export default function ManageComicsPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)

  const { data: channels } = useSuspenseQuery(channelsQuery())
  const channel = String(router.query.channel ?? '') || channels[0]?.ulid
  const params = { search, channel, limit, offset }
  const { data } = useSuspenseQuery(manageComicsQuery(params))

  return <ManageComics key={`${channel}-${search}-${page}`} channels={channels} data={data} page={page} />
}
