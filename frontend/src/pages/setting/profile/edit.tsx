import { GetStaticProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getSettingProfile } from 'api/internal/setting'
import { useFreshData } from 'components/hooks/useFreshData'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import SettingProfileEdit from 'components/templates/setting/profile/edit'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function SettingProfilePage(): React.JSX.Element {
  const query = useQuery({ queryKey: queryKeys.settingProfile, queryFn: () => toQuery(getSettingProfile()) })
  const data = useFreshData({ profile: query })

  return (
    <QueryCheck queries={[query]} data={data} title="アカウント設定">
      {(props) => <SettingProfileEdit {...props} />}
    </QueryCheck>
  )
}
