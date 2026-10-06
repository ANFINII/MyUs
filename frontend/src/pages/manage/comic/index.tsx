import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getChannels } from 'api/internal/channel'
import { getManageComics } from 'api/internal/manage/get'
import { pageParams } from 'utils/functions/common'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageComics from 'components/templates/manage/comic'

export default function ManageComicsPage(): React.JSX.Element {
  const router = useAppRouter()
  const { search, page, limit, offset } = pageParams(router.query)

  const channels = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()), enabled: router.isReady })

  const channel = router.query.channel?.toString() || channels.data?.[0]?.ulid
  const params = { search, channel, limit, offset }

  const list = useQuery({
    queryKey: queryKeys.manageComicList(params),
    queryFn: () => toQuery(getManageComics(params)),
    enabled: channels.isSuccess,
    placeholderData: keepPreviousData,
  })
  const queries = { channels, list }

  return (
    <QueryCheck title="Comic" queries={queries}>
      {(props) => <ManageComics {...props} page={page} />}
    </QueryCheck>
  )
}
