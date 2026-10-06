import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import BlogCreate from 'components/templates/manage/blog/create'

export default function BlogCreatePage(): React.JSX.Element {
  const channelsQuery = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })
  const categoriesQuery = useQuery({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()) })
  const queries = { channels: channelsQuery, categories: categoriesQuery }

  return (
    <QueryCheck title="Blog" queries={queries} fresh>
      {(props) => <BlogCreate {...props} />}
    </QueryCheck>
  )
}
