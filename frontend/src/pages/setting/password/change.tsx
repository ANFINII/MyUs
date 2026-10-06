import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getUser } from 'api/internal/user'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import PasswordChange from 'components/templates/setting/password/change'

export default function PasswordChangePage(): React.JSX.Element {
  const query = useQuery({ queryKey: queryKeys.user, queryFn: () => toQuery(getUser()) })
  const queries = { user: query }

  return (
    <QueryCheck title="パスワード変更" queries={queries}>
      <PasswordChange />
    </QueryCheck>
  )
}
