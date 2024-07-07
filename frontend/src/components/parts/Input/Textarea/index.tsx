import { useState } from 'react'
import clsx from 'clsx'
import style from './Textarea.module.scss'

interface Props {
  label?: string
  errorText?: string
  name?: string
  value?: string
  placeholder?: string
  className?: string
  error?: boolean
  required?: boolean
  disabled?: boolean
  onChange?: (value: string) => void
  children?: React.ReactNode
}

export default function Textarea(props: Props) {
  const { label, errorText, value, className, error = false, required = false, onChange, children } = props

  const [rows, setRows] = useState(value?.split('\n').length || 1)
  const [isValue, setIsValue] = useState<boolean>(false)

  const isRequired = required && !isValue
  const isErrorText = !isRequired && error

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const height = e.target.value.split('\n').length
    setRows(height)
    setIsValue(e.target.value !== '')
    onChange && onChange(e.target.value)
  }

  return (
    <div className={className}>
      {label && (
        <label htmlFor={label} className={style.label}>
          {label}
        </label>
      )}
      <textarea {...props} id={label} rows={rows} onChange={handleChange} className={clsx(style.textarea, isRequired && style.error)}>
        {children}
      </textarea>
      {isRequired && <p className={style.error_text}>※必須入力です！</p>}
      {isErrorText && <p className={style.error_text}>{errorText}</p>}
    </div>
  )
}
