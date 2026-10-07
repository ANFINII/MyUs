import { useQuery } from '@tanstack/react-query'
import { useParams } from '@tanstack/react-router'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getCategories } from 'api/internal/category'
import { getChannels } from 'api/internal/channel'
import { getManageBlog } from 'api/internal/manage/get'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import ManageBlogEdit from 'components/templates/manage/blog/edit'

export default function ManageBlogEditPage(): React.JSX.Element {
  const { ulid } = useParams({ from: '/manage/blog/$ulid' })

  const channels = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })
  const categories = useQuery({ queryKey: queryKeys.categories, queryFn: () => toQuery(getCategories()) })
  const data = useQuery({ queryKey: queryKeys.manageBlogDetail(ulid), queryFn: () => toQuery(getManageBlog(ulid)) })
  const queries = { data, channels, categories }

  return (
    <QueryCheck title="Blog" queries={queries} fresh>
      {(props) => <ManageBlogEdit {...props} />}
    </QueryCheck>
  )
}
