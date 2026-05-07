import cx from 'utils/functions/cx'
import Button from 'components/parts/Button'
import style from './PlanCard.module.scss'

export interface Plan {
  name: string
  price: number
  features: string[]
  stripeId: string
}

interface Props {
  plan: Plan
  active: boolean
  onClick: () => void
  current?: boolean
  showPurchase?: boolean
}

export default function PlanCard(props: Props): React.JSX.Element {
  const { plan, active, onClick, current = false, showPurchase = true } = props
  const { name, price, features, stripeId } = plan

  return (
    <div className={cx(style.plan, active && style.active)} onClick={onClick}>
      <div className={style.name}>
        {name}
        {current && <span className={style.current_label}>現在</span>}
      </div>
      <div className={style.price}>
        <span>¥{price.toLocaleString()}</span>
        <span className={style.price_unit}>/ 月</span>
      </div>
      <ul className={style.features}>
        {features.map((feature) => (
          <li key={feature} className={style.feature}>
            {feature}
          </li>
        ))}
      </ul>
      {showPurchase && <Button color="purple" size="l" name="購入する" value={stripeId} />}
    </div>
  )
}
