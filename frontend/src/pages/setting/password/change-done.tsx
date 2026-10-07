import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getUser } from 'api/internal/user'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import PasswordChangeDone from 'components/templates/setting/password/change-done'

export default function PasswordChangeDonePage(): React.JSX.Element {
  const { t } = useTranslation()
  const user = useQuery({ queryKey: queryKeys.user, queryFn: () => toQuery(getUser()) })
  const queries = { user }

  return (
    <QueryCheck title={t('setting.password.title')} queries={queries}>
      <PasswordChangeDone />
    </QueryCheck>
  )
}
