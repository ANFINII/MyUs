import { useSuspenseQuery } from '@tanstack/react-query'
import { paymentSubscriptionQuery, settingMypageQuery } from 'lib/query/options'
import Payment from './view'

export default function PaymentPage(): React.JSX.Element {
  const { data: mypage } = useSuspenseQuery(settingMypageQuery())
  const { data: subscription } = useSuspenseQuery(paymentSubscriptionQuery())

  return <Payment mypage={mypage} subscription={subscription} />
}
