import { useState } from 'react'
import { useRouter } from 'next/router'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import style from './Change.module.scss'
import PlanCard from '../PlanCard'
import { plans } from '../plans'

const currentPlanName = 'Free'

export default function PaymentChange(): React.JSX.Element {
  const router = useRouter()
  const [activeId, setActiveId] = useState<string>('')
  const handleBack = () => router.push('/setting/payment')
  const handleSubmit = () => router.push('/setting/payment')

  const currentStripeId = plans.find((plan) => plan.name === currentPlanName)?.stripeId ?? ''
  const isChanged = activeId !== '' && activeId !== currentStripeId

  return (
    <Main metaTitle="プラン変更">
      <div className={style.change}>
        <div className={style.current}>
          <span className={style.current_label}>現在のプラン</span>
          <span className={style.current_plan}>{currentPlanName}</span>
        </div>

        <div className={style.plans}>
          {plans.map((plan) => (
            <PlanCard
              key={plan.name}
              plan={plan}
              active={activeId === plan.stripeId}
              onClick={() => setActiveId(plan.stripeId)}
              current={plan.name === currentPlanName}
              showPurchase={false}
            />
          ))}
        </div>

        <div className={style.actions}>
          <Button color="green" size="l" name="変更する" disabled={!isChanged} onClick={handleSubmit} />
          <Button color="blue" size="l" name="キャンセル" onClick={handleBack} />
        </div>
      </div>
    </Main>
  )
}
