import { ChangeEvent } from 'react'
import cx from 'utils/functions/cx'
import style from './SpeedControl.module.scss'

interface Props {
  value: number
  className?: string
  onChange: (e: ChangeEvent<HTMLInputElement>) => void
}

export default function SpeedControl(props: Props): React.JSX.Element {
  const { value, className, onChange } = props

  return (
    <div className={cx(style.speed, className)}>
      <span>Speed</span>
      <input type="range" min="0" max="2" step="0.25" value={value} onChange={onChange} className={style.range} />
      <span>{value}</span>
    </div>
  )
}
