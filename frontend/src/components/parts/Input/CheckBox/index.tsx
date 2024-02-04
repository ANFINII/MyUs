import { useState } from 'react'
import style from 'components/parts/Input/CheckBox/CheckBox.module.scss'

interface Props {
  name?: string
  id?: string
  labelName: string
  className?: string
}

export default function CheckBox(props: Props) {
  const { name, id, labelName, className } = props

  const [checked, setChecked] = useState(true)
  const handleChange = () => setChecked(!checked)

  return (
    <div className={style.check_group + (className ? ' ' + className : '')}>
      <input type="checkbox" name={name} id={id} onClick={handleChange} className={style.checkbox} checked={checked} />
      <label htmlFor={id}>{labelName}</label>
    </div>
  )
}
