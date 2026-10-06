import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getUser } from 'api/internal/user'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Manage from 'components/templates/manage'

export default function ManagePage(): React.JSX.Element {
  const query = useQuery({ queryKey: queryKeys.user, queryFn: () => toQuery(getUser()) })
  const queries = { user: query }

  return (
    <QueryCheck title="投稿管理" queries={queries}>
      <Manage />
    </QueryCheck>
  )
}
