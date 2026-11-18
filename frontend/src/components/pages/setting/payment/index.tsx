import { useSuspenseQuery } from '@tanstack/react-query'
import { paymentPlansQuery, paymentSellerQuery, paymentSubscriptionQuery, settingMypageQuery } from 'lib/query/options'
import Payment from './view'

export default function PaymentPage(): React.JSX.Element {
  const { data: mypage } = useSuspenseQuery(settingMypageQuery())
  const { data: subscription } = useSuspenseQuery(paymentSubscriptionQuery())
  const { data: planPrices } = useSuspenseQuery(paymentPlansQuery())
  const { data: seller } = useSuspenseQuery(paymentSellerQuery())

  return <Payment mypage={mypage} subscription={subscription} planPrices={planPrices} seller={seller} />
}
