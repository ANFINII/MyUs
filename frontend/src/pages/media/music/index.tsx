import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getMusics } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import { useAppRouter } from 'components/hooks/useAppRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Musics from 'components/templates/media/music/list'

export default function MusicsPage(): React.JSX.Element {
  const router = useAppRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }

  const data = useQuery({ queryKey: queryKeys.mediaMusicList(params), queryFn: () => toQuery(getMusics(params)), enabled: router.isReady, placeholderData: keepPreviousData })
  const queries = { data }

  return (
    <QueryCheck title="Music" queries={queries}>
      {(props) => <Musics {...props} page={page} />}
    </QueryCheck>
  )
}
