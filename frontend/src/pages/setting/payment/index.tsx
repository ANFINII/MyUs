import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getSettingMypage } from 'api/internal/setting'
import QueryCheck from 'components/widgets/Status/QueryCheck'
import Payment from 'components/templates/setting/payment'

export default function PaymentPage(): React.JSX.Element {
  const query = useQuery({ queryKey: queryKeys.settingMypage, queryFn: () => toQuery(getSettingMypage()) })
  const queries = { mypage: query }

  return (
    <QueryCheck title="料金プラン" queries={queries}>
      {(props) => <Payment {...props} />}
    </QueryCheck>
  )
}
