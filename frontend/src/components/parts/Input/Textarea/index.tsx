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

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const height = e.target.value.split('\n').length
    setRows(height)
    onChange && onChange(e.target.value)
  }

  return (
    <textarea {...props} rows={rows} onChange={handleChange} className={style.textarea + (className ? ' ' + className : '')}>
      {children}
    </textarea>
  )
}
