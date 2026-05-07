import { useState } from 'react'
import { useRouter } from 'next/router'
import { MypageOut } from 'types/internal/user'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import style from './Change.module.scss'
import CurrentBanner from '../CurrentBanner'
import PlanCard from '../PlanCard'
import { plans } from '../plans'

interface Props {
  mypage: MypageOut
}

export default function PaymentChange(props: Props): React.JSX.Element {
  const { mypage } = props
  const router = useRouter()
  const [activeName, setActiveName] = useState<string>('')
  const handleBack = () => router.push('/setting/payment')
  const handleSubmit = () => router.push('/setting/payment')

  const currentPlanName = mypage.plan
  const isChanged = activeName !== '' && activeName !== currentPlanName

  return (
    <Main metaTitle="プラン変更">
      <div className={style.change}>
        <CurrentBanner planName={currentPlanName} />

        <div className={style.plans}>
          {plans.map((plan) => (
            <PlanCard
              key={plan.name}
              plan={plan}
              active={activeName === plan.name}
              onClick={() => setActiveName(plan.name)}
              current={plan.name === currentPlanName}
              disabled={plan.name === currentPlanName}
              showPurchase={false}
            />
          ))}
        </div>

        <div className={style.actions}>
          <Button color="green" name="変更する" disabled={!isChanged} onClick={handleSubmit} />
          <Button color="blue" name="キャンセル" onClick={handleBack} />
        </div>
      </div>
    </Main>
  )
}
