import { useSuspenseQuery } from '@tanstack/react-query'
import { channelsQuery, settingMypageQuery } from 'lib/query/options'
import SettingMyPageEdit from './view'

export default function SettingMypageEditPage(): React.JSX.Element {
  const { data: channels } = useSuspenseQuery(channelsQuery())
  const { data: mypage } = useSuspenseQuery(settingMypageQuery())

  return <SettingMyPageEdit channels={channels} mypage={mypage} />
}
