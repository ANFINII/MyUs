import {useState} from 'react'
import style from 'components/parts/Input/CheckBox/CheckBox.module.css'

interface Props {
  checked?: boolean
  name?: string
  id?: string
  className?: string
  children: React.ReactNode
}

export default function CheckBox(props: Props) {
  const {checked, name, id, className, children} = props
  const [checkValue, setCheckValue] = useState(checked)
  const handleChange = () => {setCheckValue(!checkValue)}

  return (
    <div className={`${style.check_group} ` + (className ? className : "" )}>
      <input type="checkbox" name={name} id={id} onClick={handleChange}
        className={style.checkbox} checked={checkValue} />
      <label htmlFor={id}>{children}</label>
    </div>
  )
}
