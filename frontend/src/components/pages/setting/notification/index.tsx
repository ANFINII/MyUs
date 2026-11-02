import { useSuspenseQuery } from '@tanstack/react-query'
import { settingNotificationQuery } from 'lib/query/options'
import SettingNotification from './view'

export default function SettingNotificationPage(): React.JSX.Element {
  const { data: userNotification } = useSuspenseQuery(settingNotificationQuery())

  return <SettingNotification userNotification={userNotification} />
}
