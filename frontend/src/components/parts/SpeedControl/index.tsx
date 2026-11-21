import { ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import cx from 'utils/functions/cx'
import style from './SpeedControl.module.scss'

const MIN_SPEED = 0.5
const MAX_SPEED = 2

interface Props {
  value: number
  className?: string
  onChange: (e: ChangeEvent<HTMLInputElement>) => void
}

export default function SpeedControl(props: Props): React.JSX.Element {
  const { value, className, onChange } = props

  const { t } = useTranslation()

  const percent = ((value - MIN_SPEED) / (MAX_SPEED - MIN_SPEED)) * 100

  return (
    <div className={cx(style.speed, className)}>
      <span className={style.label}>{t('player.speed')}</span>
      <div className={style.track}>
        <div className={style.rail}>
          <div className={style.fill} style={{ width: `${percent}%` }} />
        </div>
        <input type="range" min={MIN_SPEED} max={MAX_SPEED} step="0.25" value={value} aria-label={t('player.speed')} onChange={onChange} className={style.range} />
      </div>
      <span className={style.value}>{value.toFixed(2)}×</span>
    </div>
  )
}
