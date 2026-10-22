import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { settingNotificationQuery } from 'lib/query/options'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import SettingNotification from 'components/templates/setting/notification'

export default function SettingNotificationPage(): React.JSX.Element {
  const { t } = useTranslation()
  const userNotification = useQuery(settingNotificationQuery())
  const queries = { userNotification }

  return (
    <QueryCheck title={t('setting.notification.title')} queries={queries}>
      {(props) => <SettingNotification {...props} />}
    </QueryCheck>
  )
}
