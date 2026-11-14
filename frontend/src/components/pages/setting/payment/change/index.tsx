import { useSuspenseQuery } from '@tanstack/react-query'
import { paymentPlansQuery, settingMypageQuery } from 'lib/query/options'
import PaymentChange from './view'

export default function PaymentChangePage(): React.JSX.Element {
  const { data: mypage } = useSuspenseQuery(settingMypageQuery())
  const { data: planPrices } = useSuspenseQuery(paymentPlansQuery())

  return <PaymentChange mypage={mypage} planPrices={planPrices} />
}
