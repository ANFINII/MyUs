import { useState } from 'react'
import clsx from 'clsx'
import style from 'components/parts/Input/Textarea/Textarea.module.scss'

interface Props {
  name?: string
  value?: string
  placeholder?: string
  required?: boolean
  disabled?: boolean
  className?: string
  children?: React.ReactNode
  onChange?: (value: string) => void
}

export default function Textarea(props: Props) {
  const { className = '', children, onChange } = props

  const [rows, setRows] = useState(1)

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const height = e.target.value.split('\n').length
    setRows(height)
    onChange && onChange(e.target.value)
  }

  return (
    <textarea {...props} rows={rows} onChange={handleChange} className={clsx(style.textarea, className)}>
      {children}
    </textarea>
  )
}
