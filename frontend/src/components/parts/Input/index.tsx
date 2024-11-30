import React, { useState } from 'react'
import clsx from 'clsx'
import useAutoFocus from 'components/hooks/useAutoFocus'
import style from './Input.module.scss'

interface Props {
  label?: string
  errorText?: string
  type?: string
  name?: string
  value?: string
  defaultValue?: string
  placeholder?: string
  className?: string
  minLength?: number
  maxLength?: number
  error?: boolean
  required?: boolean
  disabled?: boolean
  autoFocus?: boolean
  onChange?: (value: string) => void
  onClick?: (event: React.MouseEvent<HTMLInputElement>) => void
}

export default function Input(props: Props) {
  const { label, errorText, value, className, error = false, required = false, autoFocus, onChange } = props

  const inputFocus = useAutoFocus()
  const [isValue, setIsValue] = useState<boolean>(false)

  const isRequired = required && !isValue && !value
  const isErrorText = !isRequired && error

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setIsValue(value !== '')
    if (onChange) onChange(value)
  }

  return (
    <div className={className}>
      {label && (
        <label htmlFor={label} className={style.label}>
          {label}
        </label>
      )}
      <input {...props} id={label} onChange={handleChange} ref={autoFocus ? inputFocus : undefined} className={clsx(style.input, isRequired && style.error)} />
      {isRequired && <p className={style.error_text}>※必須入力です！</p>}
      {isErrorText && <p className={style.error_text}>{errorText}</p>}
    </div>
  )
}
