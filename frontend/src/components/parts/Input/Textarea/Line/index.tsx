import { useState } from 'react'
import style from 'components/parts/Input/Textarea/Textarea.module.scss'

interface Props {
  id?: string
  className?: string
  name?: string
  value?: string
  placeholder?: string
  required?: boolean
  disabled?: boolean
  onChange?: (value: string) => void
  children?: React.ReactNode
}

export default function Textarea(props: Props) {
  const { className, onChange, children } = props

  const [rows, setRows] = useState(1)
  const [lineHeight, setLineHeight] = useState(16)

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const lines = (e.target.value + '\n').match(/\n/g)?.length || 1
    setRows(lines)
    onChange && onChange(e.target.value)
    setLineHeight(e.target.scrollHeight / lines)
  }

  return (
    <textarea {...props} rows={rows} onChange={handleChange} style={{ lineHeight: `${lineHeight}px` }} className={style.line + (className ? ' ' + className : '')}>
      {children}
    </textarea>
  )
}
