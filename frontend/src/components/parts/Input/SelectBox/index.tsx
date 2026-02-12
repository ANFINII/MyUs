import { ChangeEvent } from 'react'
import { Option } from 'types/internal/other'
import Select from 'components/parts/Select'
import style from './SelectBox.module.scss'

interface Props {
  label?: string
  name?: string
  value: string
  options: Option[]
  placeholder?: string
  className?: string
  onChange: (e: ChangeEvent<HTMLSelectElement>) => void
}

export default function SelectBox(props: Props): React.JSX.Element {
  const { label, className } = props

  return (
    <div className={className}>
      {label && (
        <label htmlFor={label} className={style.label}>
          {label}
        </label>
      )}
      <div className={style.select_box}>
        <Select {...props} id={label} className={style.select} />
      </div>
    </div>
  )
}
