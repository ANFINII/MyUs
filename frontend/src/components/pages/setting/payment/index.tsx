import { useSuspenseQuery } from '@tanstack/react-query'
import { settingMypageQuery } from 'lib/query/options'
import Payment from './view'

export default function PaymentPage(): React.JSX.Element {
  const { data: mypage } = useSuspenseQuery(settingMypageQuery())

  return <Payment mypage={mypage} />
}
