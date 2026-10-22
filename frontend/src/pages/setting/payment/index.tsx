import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { settingMypageQuery } from 'lib/query/options'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Payment from 'components/templates/setting/payment'

export default function PaymentPage(): React.JSX.Element {
  const { t } = useTranslation()
  const mypage = useQuery(settingMypageQuery())
  const queries = { mypage }

  return (
    <QueryCheck title={t('setting.payment.title')} queries={queries}>
      {(props) => <Payment {...props} />}
    </QueryCheck>
  )
}
