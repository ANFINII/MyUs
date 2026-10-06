import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getSettingMypage } from 'api/internal/setting'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import PaymentChange from 'components/templates/setting/payment/change'

export default function PaymentChangePage(): React.JSX.Element {
  const query = useQuery({ queryKey: queryKeys.settingMypage, queryFn: () => toQuery(getSettingMypage()) })
  const queries = { mypage: query }

  return (
    <QueryCheck title="プラン変更" queries={queries}>
      {(props) => <PaymentChange {...props} />}
    </QueryCheck>
  )
}
