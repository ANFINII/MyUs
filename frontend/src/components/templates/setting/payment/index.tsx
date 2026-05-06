import { useState } from 'react'
import { useRouter } from 'next/router'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import style from './Payment.module.scss'
import PlanCard, { Plan } from './PlanCard'

const plans: Plan[] = [
  {
    name: 'Basic',
    price: 550,
    features: ['個別広告表示 1つ', '全体広告 非表示'],
    stripeId: 'price_1K9VSxCHdDAlRliqOZnYuctl',
  },
  {
    name: 'Standard',
    price: 880,
    features: ['個別広告表示 3つ', '全体広告 非表示'],
    stripeId: 'price_1K9VTbCHdDAlRliq3YNA768b',
  },
  {
    name: 'Premium',
    price: 1200,
    features: ['個別広告表示 4つ', '全体広告 非表示', '楽曲ダウンロード'],
    stripeId: 'price_1K9VU9CHdDAlRliqXsIS6GC4',
  },
]

export default function Payment(): React.JSX.Element {
  const router = useRouter()
  const [activeId, setActiveId] = useState<string>('')
  const handleChange = () => router.push('/setting/payment/change')
  const handleCancel = () => router.push('/setting/payment/cancel')

  return (
    <Main metaTitle="料金プラン">
      <div className={style.payment}>
        <div className={style.plans}>
          {plans.map((plan) => (
            <PlanCard key={plan.name} plan={plan} active={activeId === plan.stripeId} onClick={() => setActiveId(plan.stripeId)} />
          ))}
        </div>

        <div className={style.current}>
          <p className={style.current_label}>現在のプランを変更</p>
          <div className={style.current_actions}>
            <Button color="green" size="m" name="プランを変更" onClick={handleChange} />
            <Button color="red" size="m" name="解約する" onClick={handleCancel} />
          </div>
        </div>
      </div>
    </Main>
  )
}
