import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { userQuery } from 'lib/query/options'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Manage from 'components/templates/manage'

export default function ManagePage(): React.JSX.Element {
  const { t } = useTranslation()
  const user = useQuery(userQuery())
  const queries = { user }

  return (
    <QueryCheck title={t('manage.title')} queries={queries}>
      <Manage />
    </QueryCheck>
  )
}
