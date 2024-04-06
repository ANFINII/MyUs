import { ChangeEvent } from 'react'
import clsx from 'clsx'
import style from 'components/parts/Input/CheckBox/CheckBox.module.scss'

interface Props {
  label: string
  className?: string
  checked?: boolean
  onChange?: (checked: boolean) => void
}

export default function CheckBox(props: Props) {
  const { label, className = '', checked, onChange } = props

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (onChange) {
      onChange(e.target.checked)
    }
  }

  return (
    <div className={clsx(style.check_group, className)}>
      <input id={label} type="checkbox" className={style.checkbox} defaultChecked={checked} onChange={handleChange} />
      <label htmlFor={label}>{label}</label>
    </div>
  )
}
