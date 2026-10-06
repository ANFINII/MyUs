import { GetStaticProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getSettingNotification } from 'api/internal/setting'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import SettingNotification from 'components/templates/setting/notification'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function SettingNotificationPage(): React.JSX.Element {
  const query = useQuery({
    queryKey: queryKeys.settingNotification,
    queryFn: () => toQuery(getSettingNotification()),
  })

  const data = query.isFetchedAfterMount && query.data ? { userNotification: query.data } : undefined

  return (
    <QueryCheck queries={[query]} data={data} title="通知設定">
      {(props) => <SettingNotification {...props} />}
    </QueryCheck>
  )
}
