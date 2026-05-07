import { useState } from 'react'
import { useRouter } from 'next/router'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import style from './Payment.module.scss'
import PlanCard from './PlanCard'
import { plans } from './plans'

const currentPlanName = 'Free'

export default function Payment(): React.JSX.Element {
  const router = useRouter()
  const [activeId, setActiveId] = useState<string>('')
  const handleChange = () => router.push('/setting/payment/change')
  const handleCancel = () => router.push('/setting/payment/cancel')

  return (
    <Main metaTitle="料金プラン">
      <div className={style.payment}>
        <div className={style.current}>
          <span className={style.current_label}>現在のプラン</span>
          <span className={style.current_plan}>{currentPlanName}</span>
        </div>

        <div className={style.plans}>
          {plans.map((plan) => (
            <PlanCard key={plan.name} plan={plan} active={activeId === plan.stripeId} onClick={() => setActiveId(plan.stripeId)} />
          ))}
        </div>

        <div className={style.actions}>
          <Button color="green" size="m" name="プランを変更" onClick={handleChange} />
          <Button color="red" size="m" name="解約する" onClick={handleCancel} />
        </div>
      </div>
    </Main>
  )
}
