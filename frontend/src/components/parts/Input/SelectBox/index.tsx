import { ChangeEvent } from 'react'
import { Option } from 'types/internal/other'
import cx from 'utils/functions/cx'
import Select from 'components/parts/Select'
import style from './SelectBox.module.scss'

interface Props {
  label?: string
  value: string
  name?: string
  placeholder?: string
  error?: string
  className?: string
  options: Option[]
  required?: boolean
  disabled?: boolean
  onChange?: (e: ChangeEvent<HTMLSelectElement>) => void
}

export default function SelectBox(props: Props): React.JSX.Element {
  const { label, value, error, className, required = false, ...rest } = props

  const isError = !!error || (error === '' && required && !value)

  return (
    <div className={cx(style.box, className)}>
      {label && (
        <label htmlFor={label} className={style.label}>
          {label}
          {required && <span className={style.required}>*</span>}
        </label>
      )}
      <div className={style.select_box}>
        <Select {...rest} value={value} id={label} className={cx(style.select, isError && style.error)} />
      </div>
      {error && <p className={style.error_text}>{error}</p>}
    </div>
  )
}
