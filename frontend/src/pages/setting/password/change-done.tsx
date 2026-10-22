import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { userQuery } from 'lib/query/options'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import PasswordChangeDone from 'components/templates/setting/password/change-done'

export default function PasswordChangeDonePage(): React.JSX.Element {
  const { t } = useTranslation()
  const user = useQuery(userQuery())
  const queries = { user }

  return (
    <QueryCheck title={t('setting.password.title')} queries={queries}>
      <PasswordChangeDone />
    </QueryCheck>
  )
}
