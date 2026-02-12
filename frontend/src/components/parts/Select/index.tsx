import { ChangeEvent } from 'react'
import { Option } from 'types/internal/other'

interface Props {
  id?: string
  name?: string
  value: string
  options: Option[]
  placeholder?: string
  className?: string
  onChange: (e: ChangeEvent<HTMLSelectElement>) => void
}

export default function Select(props: Props): React.JSX.Element {
  const { options, placeholder } = props

  return (
    <select {...props}>
      {placeholder && (
        <option value="" hidden>
          {placeholder}
        </option>
      )}
      {options.map((option) => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  )
}
