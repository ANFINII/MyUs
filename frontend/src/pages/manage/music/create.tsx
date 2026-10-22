import { useQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery } from 'lib/query/options'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import MusicCreate from 'components/templates/manage/music/create'

export default function MusicCreatePage(): React.JSX.Element {
  const channels = useQuery(channelsQuery())
  const categories = useQuery(categoriesQuery())
  const queries = { channels, categories }

  return (
    <QueryCheck title="Music" queries={queries}>
      {(props) => <MusicCreate {...props} />}
    </QueryCheck>
  )
}
