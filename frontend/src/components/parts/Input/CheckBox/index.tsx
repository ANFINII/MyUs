import { useState } from 'react'
import clsx from 'clsx'
import style from 'components/parts/Input/CheckBox/CheckBox.module.scss'

interface Props {
  name?: string
  label: string
  className?: string
}

export default function CheckBox(props: Props) {
  const { label, className = '' } = props

  const [checked, setChecked] = useState(true)
  const handleChange = () => setChecked(!checked)

  return (
    <div className={clsx(style.check_group, className)}>
      <input {...props} id={label} type="checkbox" onClick={handleChange} className={style.checkbox} checked={checked} />
      <label htmlFor={label}>{label}</label>
    </div>
  )
}
