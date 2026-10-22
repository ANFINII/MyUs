import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { userQuery } from 'lib/query/options'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import PasswordChange from 'components/templates/setting/password/change'

export default function PasswordChangePage(): React.JSX.Element {
  const { t } = useTranslation()
  const user = useQuery(userQuery())
  const queries = { user }

  return (
    <QueryCheck title={t('setting.password.title')} queries={queries}>
      <PasswordChange />
    </QueryCheck>
  )
}
