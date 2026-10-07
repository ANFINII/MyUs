import { keepPreviousData, useQuery } from '@tanstack/react-query'
import { useSearch } from '@tanstack/react-router'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getMusics } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Musics from 'components/templates/media/music/list'

export default function MusicsPage(): React.JSX.Element {
  const query = useSearch({ strict: false })
  const { search, page, limit, offset } = pageParams(query)
  const params = { search, limit, offset }

  const data = useQuery({ queryKey: queryKeys.mediaMusicList(params), queryFn: () => toQuery(getMusics(params)), placeholderData: keepPreviousData })
  const queries = { data }

  return (
    <QueryCheck title="Music" queries={queries}>
      {(props) => <Musics {...props} page={page} />}
    </QueryCheck>
  )
}
