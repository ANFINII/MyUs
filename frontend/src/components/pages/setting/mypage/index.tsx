import { useSuspenseQuery } from '@tanstack/react-query'
import { channelsQuery, settingMypageQuery } from 'lib/query/options'
import SettingMyPage from './view'

export default function SettingMypagePage(): React.JSX.Element {
  const { data: channels } = useSuspenseQuery(channelsQuery())
  const { data: mypage } = useSuspenseQuery(settingMypageQuery())

  return <SettingMyPage channels={channels} mypage={mypage} />
}
