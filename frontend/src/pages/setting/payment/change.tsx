import { GetStaticProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getSettingMypage } from 'api/internal/setting'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import PaymentChange from 'components/templates/setting/payment/change'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function PaymentChangePage(): React.JSX.Element {
  const query = useQuery({ queryKey: queryKeys.settingMypage, queryFn: () => toQuery(getSettingMypage()) })

  const data = query.data && { mypage: query.data }

  return (
    <QueryCheck queries={[query]} data={data} title="プラン変更">
      {(props) => <PaymentChange {...props} />}
    </QueryCheck>
  )
}
