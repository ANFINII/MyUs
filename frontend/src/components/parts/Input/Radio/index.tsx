import clsx from 'clsx'
import style from './Radio.module.scss'

interface Props {
  label: string
  value: string
  checked?: boolean
  className?: string
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void
}

export default function Radio(props: Props): JSX.Element {
  const { label, value, className = '', checked, onChange } = props

  return (
    <div className={clsx(style.radio, className)}>
      <input type="radio" value={value} checked={checked} id={value} onChange={onChange} />
      <label htmlFor={value}>{label}</label>
    </div>
  )
}
