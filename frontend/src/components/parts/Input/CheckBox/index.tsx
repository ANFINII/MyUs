import { useState } from 'react'
import clsx from 'clsx'
import style from 'components/parts/Input/CheckBox/CheckBox.module.scss'

interface Props {
  id?: string
  name?: string
  labelName: string
  className?: string
}

export default function CheckBox(props: Props) {
  const { id, name, labelName, className = '' } = props

  const [checked, setChecked] = useState(true)
  const handleChange = () => setChecked(!checked)

  return (
    <div className={clsx(style.check_group, className)}>
      <input type="checkbox" name={name} id={id} onClick={handleChange} className={style.checkbox} checked={checked} />
      <label htmlFor={id}>{labelName}</label>
    </div>
  )
}
