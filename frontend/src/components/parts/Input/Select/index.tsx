import { useState } from 'react'
import { Option } from 'types/internal/other'
import style from 'components/parts/Input/Select/Select.module.css'

interface Props {
  className?: string
  name?: string
  value?: string | number
  options: Option[]
  placeholder?: string
}

export default function Select(props: Props) {
  const { className, name, value, placeholder, options } = props

  const [changeValue, setChangeValue] = useState(value)

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setChangeValue(e.target.value)
  }

  return (
    <label className={style.select + (className ? ' ' + className : '')}>
      <select name={name} value={changeValue} onChange={handleChange}>
        {placeholder && (
          <option value="" disabled selected hidden>
            {placeholder}
          </option>
        )}
        {options.map(({ label, value }) => (
          <option key={value} value={value}>
            {label}
          </option>
        ))}
      </select>
    </label>
  )
}
