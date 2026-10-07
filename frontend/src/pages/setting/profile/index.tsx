import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getSettingProfile } from 'api/internal/setting'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import SettingProfile from 'components/templates/setting/profile'

export default function SettingProfilePage(): React.JSX.Element {
  const { t } = useTranslation()
  const profile = useQuery({ queryKey: queryKeys.settingProfile, queryFn: () => toQuery(getSettingProfile()) })
  const queries = { profile }

  return (
    <QueryCheck title={t('setting.profile.title')} queries={queries}>
      {(props) => <SettingProfile {...props} />}
    </QueryCheck>
  )
}
