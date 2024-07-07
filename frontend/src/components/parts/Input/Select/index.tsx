import { Option } from 'types/internal/other'
import style from './Select.module.scss'

interface Props {
  label?: string
  name?: string
  value: string | number
  options: Option[]
  placeholder?: string
  className?: string
  onChange: (value: string) => void
}

export default function Select(props: Props) {
  const { label, name, value, options, placeholder, className = '', onChange } = props

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onChange(e.target.value)
  }

  return (
    <div className={className}>
      {label && (
        <label htmlFor={label} className={style.label}>
          {label}
        </label>
      )}
      <select id={label} name={name} value={value} onChange={handleChange} className={style.select}>
        {placeholder && (
          <option value="" disabled selected hidden>
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
  )
}
