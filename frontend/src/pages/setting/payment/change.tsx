import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { settingMypageQuery } from 'lib/query/options'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import PaymentChange from 'components/templates/setting/payment/change'

export default function PaymentChangePage(): React.JSX.Element {
  const { t } = useTranslation()
  const mypage = useQuery(settingMypageQuery())
  const queries = { mypage }

  return (
    <QueryCheck title={t('setting.payment.changeTitle')} queries={queries}>
      {(props) => <PaymentChange {...props} />}
    </QueryCheck>
  )
}
