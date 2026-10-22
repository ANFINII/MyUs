import { useQuery } from '@tanstack/react-query'
import { musicsQuery } from 'lib/query/options'
import { pageParams } from 'utils/functions/common'
import { useRouter } from 'components/hooks/useRouter'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Musics from 'components/templates/media/music/list'

export default function MusicsPage(): React.JSX.Element {
  const router = useRouter()
  const { search, page, limit, offset } = pageParams(router.query)
  const params = { search, limit, offset }

  const data = useQuery(musicsQuery(params))
  const queries = { data }

  return (
    <QueryCheck title="Music" queries={queries}>
      {(props) => <Musics {...props} page={page} />}
    </QueryCheck>
  )
}
