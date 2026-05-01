import React, { ChangeEvent, useState } from 'react'
import cx from 'utils/functions/cx'
import { useAutoFocus } from 'components/hooks/useAutoFocus'
import style from './Input.module.scss'

interface Props {
  label?: string
  value?: string
  type?: string
  name?: string
  defaultValue?: string
  placeholder?: string
  error?: string
  className?: string
  minLength?: number
  maxLength?: number
  required?: boolean
  disabled?: boolean
  autoFocus?: boolean
  onChange?: (e: ChangeEvent<HTMLInputElement>) => void
  onClick?: (event: React.MouseEvent<HTMLInputElement>) => void
}

export default function Input(props: Props): React.JSX.Element {
  const { label, error, className, required = false, disabled = false, autoFocus, onChange, ...rest } = props

  const inputFocus = useAutoFocus()
  const [isValue, setIsValue] = useState<boolean>(false)

  const isError = !!error || (error === '' && required && !isValue && !rest.value)

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setIsValue(value !== '')
    onChange?.(e)
  }

  return (
    <div className={cx(style.box, className)}>
      {label && (
        <label htmlFor={label} className={style.label}>
          {label}
          {required && <span className={style.required}>*</span>}
        </label>
      )}
      <input
        {...rest}
        id={label}
        required={required}
        disabled={disabled}
        onChange={handleChange}
        ref={autoFocus ? inputFocus : undefined}
        className={cx(style.input, isError && style.error, disabled && style.disabled)}
      />
      {error && <p className={style.error_text}>{error}</p>}
    </div>
  )
}
