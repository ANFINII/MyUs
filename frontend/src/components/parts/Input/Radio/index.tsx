import clsx from 'clsx'
import style from './Radio.module.scss'

interface Props {
  label: string
  id?: string
  name?: string
  value?: string
  checked?: boolean
  className?: string
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void
}

export default function Radio(props: Props): JSX.Element {
  const { label, id, value, className = '' } = props

  return (
    <div className={clsx(style.radio, className)}>
      <input {...props} type="radio" id={id || value} />
      <label htmlFor={id || value} className={style.label}>{label}</label>
    </div>
  )
}
