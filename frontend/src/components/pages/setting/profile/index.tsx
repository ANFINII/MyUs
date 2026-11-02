import { useSuspenseQuery } from '@tanstack/react-query'
import { settingProfileQuery } from 'lib/query/options'
import SettingProfile from './view'

export default function SettingProfilePage(): React.JSX.Element {
  const { data: profile } = useSuspenseQuery(settingProfileQuery())

  return <SettingProfile profile={profile} />
}
