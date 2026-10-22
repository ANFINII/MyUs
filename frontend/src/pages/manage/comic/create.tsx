import { useQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery } from 'lib/query/options'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ComicCreate from 'components/templates/manage/comic/create'

export default function ComicCreatePage(): React.JSX.Element {
  const channels = useQuery(channelsQuery())
  const categories = useQuery(categoriesQuery())
  const queries = { channels, categories }

  return (
    <QueryCheck title="Comic" queries={queries}>
      {(props) => <ComicCreate {...props} />}
    </QueryCheck>
  )
}
