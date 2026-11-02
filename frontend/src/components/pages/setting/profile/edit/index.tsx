import { useSuspenseQuery } from '@tanstack/react-query'
import { settingProfileQuery } from 'lib/query/options'
import SettingProfileEdit from './view'

export default function SettingProfilePage(): React.JSX.Element {
  const { data: profile } = useSuspenseQuery(settingProfileQuery())

  return <SettingProfileEdit profile={profile} />
}
