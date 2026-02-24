import { ChangeEvent } from 'react'
import style from './SpeedControl.module.scss'

interface Props {
  value: number
  onChange: (e: ChangeEvent<HTMLInputElement>) => void
}

export default function SpeedControl(props: Props): React.JSX.Element {
  const { value, onChange } = props

  return (
    <div className={style.speed}>
      <span>Speed</span>
      <input type="range" min="0" max="2" step="0.25" value={value} onChange={onChange} className={style.range} />
      <span>{value}</span>
    </div>
  )
}
