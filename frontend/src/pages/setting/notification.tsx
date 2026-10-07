import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getSettingNotification } from 'api/internal/setting'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import SettingNotification from 'components/templates/setting/notification'

export default function SettingNotificationPage(): React.JSX.Element {
  const { t } = useTranslation()
  const userNotification = useQuery({ queryKey: queryKeys.settingNotification, queryFn: () => toQuery(getSettingNotification()) })
  const queries = { userNotification }

  return (
    <QueryCheck title={t('setting.notification.title')} queries={queries} fresh>
      {(props) => <SettingNotification {...props} />}
    </QueryCheck>
  )
}
