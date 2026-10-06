import { GetStaticProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getChannels } from 'api/internal/channel'
import { getSettingMypage } from 'api/internal/setting'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import SettingMyPage from 'components/templates/setting/mypage'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function SettingMypagePage(): React.JSX.Element {
  const mypageQuery = useQuery({
    queryKey: queryKeys.settingMypage,
    queryFn: () => toQuery(getSettingMypage()),
  })

  const channelsQuery = useQuery({
    queryKey: queryKeys.channels,
    queryFn: () => toQuery(getChannels()),
  })

  const channels = channelsQuery.isError ? [] : channelsQuery.data
  const data = mypageQuery.data && channels ? { mypage: mypageQuery.data, channels } : undefined

  return (
    <QueryCheck queries={[mypageQuery]} data={data} title="マイページ設定">
      {(props) => <SettingMyPage {...props} />}
    </QueryCheck>
  )
}
