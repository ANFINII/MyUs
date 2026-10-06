import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getChannels } from 'api/internal/channel'
import { getSettingMypage } from 'api/internal/setting'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import SettingMyPage from 'components/templates/setting/mypage'

export default function SettingMypagePage(): React.JSX.Element {
  const channels = useQuery({ queryKey: queryKeys.channels, queryFn: () => toQuery(getChannels()) })
  const mypage = useQuery({ queryKey: queryKeys.settingMypage, queryFn: () => toQuery(getSettingMypage()) })
  const queries = { mypage, channels }

  return (
    <QueryCheck title="マイページ設定" queries={queries}>
      {(props) => <SettingMyPage {...props} />}
    </QueryCheck>
  )
}
