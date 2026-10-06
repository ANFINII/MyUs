import { GetStaticProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getSettingMypage } from 'api/internal/setting'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Payment from 'components/templates/setting/payment'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function PaymentPage(): React.JSX.Element {
  const query = useQuery({ queryKey: queryKeys.settingMypage, queryFn: () => toQuery(getSettingMypage()) })
  const queries = { mypage: query }

  return (
    <QueryCheck queries={queries} title="料金プラン">
      {(props) => <Payment {...props} />}
    </QueryCheck>
  )
}
