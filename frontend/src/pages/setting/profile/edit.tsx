import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { settingProfileQuery } from 'lib/query/options'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import SettingProfileEdit from 'components/templates/setting/profile/edit'

export default function SettingProfilePage(): React.JSX.Element {
  const { t } = useTranslation()
  const profile = useQuery(settingProfileQuery())
  const queries = { profile }

  return (
    <QueryCheck title={t('setting.profile.title')} queries={queries}>
      {(props) => <SettingProfileEdit {...props} />}
    </QueryCheck>
  )
}
