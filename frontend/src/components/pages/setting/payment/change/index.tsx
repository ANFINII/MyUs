import { useSuspenseQuery } from '@tanstack/react-query'
import { settingMypageQuery } from 'lib/query/options'
import PaymentChange from './view'

export default function PaymentChangePage(): React.JSX.Element {
  const { data: mypage } = useSuspenseQuery(settingMypageQuery())

  return <PaymentChange mypage={mypage} />
}
