import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { channelsQuery, settingMypageQuery } from 'lib/query/options'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import SettingMyPageEdit from 'components/templates/setting/mypage/edit'

export default function SettingMypageEditPage(): React.JSX.Element {
  const { t } = useTranslation()
  const channels = useQuery(channelsQuery())
  const mypage = useQuery(settingMypageQuery())
  const queries = { mypage, channels }

  return (
    <QueryCheck title={t('setting.mypage.title')} queries={queries}>
      {(props) => <SettingMyPageEdit {...props} />}
    </QueryCheck>
  )
}
