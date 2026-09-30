import { ChangeEvent } from 'react'
import cx from 'utils/functions/cx'
import style from './Radio.module.scss'

interface Props {
  label: string
  id?: string
  name?: string
  value?: string
  checked?: boolean
  className?: string
  onChange?: (e: ChangeEvent<HTMLInputElement>) => void
}

export default function Radio(props: Props): React.JSX.Element {
  const { label, id, value, className, ...rest } = props

  return (
    <div className={cx(style.radio, className)}>
      <input {...rest} type="radio" id={id || value} value={value} />
      <label htmlFor={id || value} className={style.label}>
        {label}
      </label>
    </div>
  )
}
