import { useQuery } from '@tanstack/react-query'
import { categoriesQuery, channelsQuery } from 'lib/query/options'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import BlogCreate from 'components/templates/manage/blog/create'

export default function BlogCreatePage(): React.JSX.Element {
  const channels = useQuery(channelsQuery())
  const categories = useQuery(categoriesQuery())
  const queries = { channels, categories }

  return (
    <QueryCheck title="Blog" queries={queries}>
      {(props) => <BlogCreate {...props} />}
    </QueryCheck>
  )
}
