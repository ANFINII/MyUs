import { useState } from 'react'
import clsx from 'clsx'
import style from 'components/parts/Input/Textarea/Textarea.module.scss'

interface Props {
  label?: string
  helpText?: string
  name?: string
  value?: string
  placeholder?: string
  required?: boolean
  disabled?: boolean
  error?: boolean
  className?: string
  onChange?: (value: string) => void
  children?: React.ReactNode
}

export default function Textarea(props: Props) {
  const { label, helpText, className = '', onChange, children, required, error } = props

  const [rows, setRows] = useState(1)
  const [isValue, setIsValue] = useState<boolean>(false)

  const isRequired = required && !isValue
  const isHelpText = !isRequired && error

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
      {isRequired && <p className={style.help_text}>※必須入力です！</p>}
      {isHelpText && <p className={style.help_text}>{helpText}</p>}
    </div>
  )
}
