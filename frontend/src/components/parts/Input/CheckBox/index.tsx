import { ChangeEvent } from 'react'
import clsx from 'clsx'
import style from './CheckBox.module.scss'

interface Props {
  label: string
  id?: string
  name?: string
  className?: string
  checked?: boolean
  defaultChecked?: boolean
  onChange?: (e: ChangeEvent<HTMLInputElement>) => void
}

export default function CheckBox(props: Props): JSX.Element {
  const { label, id, className = '' } = props

  return (
    <div className={clsx(style.checkbox, className)}>
      <input {...props} type="checkbox" id={id || label} className={style.input} />
      <label htmlFor={id || label} className={style.label}>{label}</label>
    </div>
  )
}
