import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from '@tanstack/react-router'
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

  const navigate = useNavigate()
  const { t } = useTranslation()
  const [activeName, setActiveName] = useState<string>('')
  const handleBack = () => navigate({ to: '/setting/payment' })
  const handleSubmit = () => navigate({ to: '/setting/payment' })

  const currentPlanName = mypage.plan
  const isChanged = activeName !== '' && activeName !== currentPlanName

  return (
    <Main metaTitle={t('setting.payment.changeTitle')}>
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
              showPurchase={false}
            />
          ))}
        </div>

        <div className={style.actions}>
          <Button color="green" name={t('setting.button.change')} disabled={!isChanged} onClick={handleSubmit} />
          <Button color="blue" name={t('setting.button.cancel')} onClick={handleBack} />
        </div>
      </div>
    </Main>
  )
}
