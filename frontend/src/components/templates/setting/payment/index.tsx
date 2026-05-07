import { useRouter } from 'next/router'
import { MypageOut } from 'types/internal/user'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import CurrentBanner from './CurrentBanner'
import style from './Payment.module.scss'
import PlanCard from './PlanCard'
import { plans } from './plans'

interface Props {
  mypage: MypageOut
}

export default function Payment(props: Props): React.JSX.Element {
  const { mypage } = props
  const router = useRouter()
  const handleChange = () => router.push('/setting/payment/change')

  const currentPlanName = mypage.plan
  const purchasable = plans.filter((plan) => plan.stripeId !== '')
  const isPaid = currentPlanName !== 'Free'

  return (
    <Main metaTitle="料金プラン">
      <div className={style.payment}>
        <CurrentBanner planName={currentPlanName} />

        <div className={style.plans}>
          {purchasable.map((plan) => (
            <PlanCard key={plan.name} plan={plan} active={currentPlanName === plan.name} purchaseDisabled={isPaid} />
          ))}
        </div>

        {isPaid && (
          <div className={style.actions}>
            <Button color="green" size="m" name="プランを変更" onClick={handleChange} />
          </div>
        )}
      </div>
    </Main>
  )
}
