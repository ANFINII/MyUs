import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getUser } from 'api/internal/user'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Manage from 'components/templates/manage'

export default function ManagePage(): React.JSX.Element {
  const { t } = useTranslation()
  const user = useQuery({ queryKey: queryKeys.user, queryFn: () => toQuery(getUser()) })
  const queries = { user }

  return (
    <QueryCheck title={t('manage.title')} queries={queries}>
      <Manage />
    </QueryCheck>
  )
}
