import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getUser } from 'api/internal/user'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import PasswordChangeDone from 'components/templates/setting/password/change-done'

export default function PasswordChangeDonePage(): React.JSX.Element {
  const query = useQuery({ queryKey: queryKeys.user, queryFn: () => toQuery(getUser()) })
  const queries = { user: query }

  return (
    <QueryCheck title="パスワード変更" queries={queries}>
      <PasswordChangeDone />
    </QueryCheck>
  )
}
