import clsx from 'clsx'
import { Option } from 'types/internal/other'
import style from 'components/parts/Input/Select/Select.module.scss'

interface Props {
  name?: string
  value: string | number
  options: Option[]
  placeholder?: string
  className?: string
  onChange: (value: string) => void
}

export default function Select(props: Props) {
  const { name, value, options, placeholder, className = '', onChange } = props

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onChange(e.target.value)
  }

  return (
    <label className={clsx(style.select, className)}>
      <select name={name} value={value} onChange={handleChange}>
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
