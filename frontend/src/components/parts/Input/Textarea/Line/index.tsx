import { useState } from 'react'
import clsx from 'clsx'
import style from '../Textarea.module.scss'

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

export default function TextareaLine(props: Props) {
  const { className = '', children, onChange } = props

  const [rows, setRows] = useState(1)
  const [lineHeight, setLineHeight] = useState(16)

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const lines = (e.target.value + '\n').match(/\n/g)?.length || 1
    setRows(lines)
    if (onChange) onChange(e.target.value)
    setLineHeight(e.target.scrollHeight / lines)
  }

  return (
    <textarea {...props} rows={rows} onChange={handleChange} style={{ lineHeight: `${lineHeight}px` }} className={clsx(style.line, className)}>
      {children}
    </textarea>
  )
}
