import { useTranslation } from 'react-i18next'
import cx from 'utils/functions/cx'
import Button from 'components/parts/Button'
import style from './PlanCard.module.scss'

export interface Plan {
  name: string
  price: number
  features: PlanFeature[]
}

export interface PlanFeature {
  key: 'individualAds' | 'hideGlobalAds' | 'musicDownload' | 'basic' | 'withAds'
  count?: number
}

interface Props {
  plan: Plan
  active: boolean
  current?: boolean
  showPurchase?: boolean
  disabled?: boolean
  loading?: boolean
  onClick?: () => void
  onPurchase?: (plan: string) => void
}

export default function PlanCard(props: Props): React.JSX.Element {
  const { plan, active, onClick, onPurchase, current = false, showPurchase = true, disabled = false, loading = false } = props
  const { name, price, features } = plan

  const { t } = useTranslation()

  const handleClick = current ? undefined : onClick
  const handlePurchase = () => onPurchase?.(name)

  return (
    <div className={cx(style.plan, active && style.active, handleClick && style.clickable, current && style.current)} onClick={handleClick}>
      <div className={style.name}>
        {name}
        {current && <span className={style.current_label}>{t('setting.payment.current')}</span>}
      </div>
      <div className={style.price}>
        <span>¥{price.toLocaleString()}</span>
        <span className={style.price_unit}>{t('setting.payment.perMonth')}</span>
      </div>
      <ul className={style.features}>
        {features.map((feature) => (
          <li key={feature.key} className={style.feature}>
            {t(`setting.payment.features.${feature.key}`, { count: feature.count })}
          </li>
        ))}
      </ul>
      {showPurchase && name !== 'Free' && <Button color="purple" size="l" name={t('setting.payment.purchase')} disabled={disabled} loading={loading} onClick={handlePurchase} />}
    </div>
  )
}
