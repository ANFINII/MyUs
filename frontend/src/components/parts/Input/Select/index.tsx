import { ChangeEvent } from 'react'
import { Option } from 'types/internal/other'
import style from './Select.module.scss'

interface Props {
  label?: string
  name?: string
  value: string | number
  options: Option[]
  placeholder?: string
  className?: string
  onChange: (e: ChangeEvent<HTMLSelectElement>) => void
}

export default function Select(props: Props): JSX.Element {
  const { label, name, value, options, placeholder, className = '', onChange } = props

  return (
    <div className={className}>
      {label && (
        <label htmlFor={label} className={style.label}>
          {label}
        </label>
      )}
      <div className={style.select_box}>
        <select id={label} name={name} value={value} onChange={onChange} className={style.select}>
          {placeholder && (
            <option value="" hidden>
              {placeholder}
            </option>
          )}
          {options.map((option, index) => (
            <option key={index} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  )
}
