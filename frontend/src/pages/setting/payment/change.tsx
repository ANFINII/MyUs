import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getSettingMypage } from 'api/internal/setting'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import PaymentChange from 'components/templates/setting/payment/change'

export default function PaymentChangePage(): React.JSX.Element {
  const { t } = useTranslation()
  const mypage = useQuery({ queryKey: queryKeys.settingMypage, queryFn: () => toQuery(getSettingMypage()) })
  const queries = { mypage }

  return (
    <QueryCheck title={t('setting.payment.changeTitle')} queries={queries}>
      {(props) => <PaymentChange {...props} />}
    </QueryCheck>
  )
}
