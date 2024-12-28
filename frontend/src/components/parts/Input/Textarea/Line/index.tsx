import { useEffect, useRef } from 'react'
import clsx from 'clsx'
import style from '../Textarea.module.scss'

interface Props {
  label?: string
  name?: string
  value?: string
  defaultValue?: string
  placeholder?: string
  className?: string
  height?: number
  error?: boolean
  required?: boolean
  disabled?: boolean
  onChange?: (value: string) => void
}

export default function TextareaLine(props: Props) {
  const { label, value, className, height, onChange } = props

  const ref = useRef<HTMLTextAreaElement>(null)

  const adjustHeight = (height?: number) => {
    if (ref.current) {
      ref.current.style.height = height ? `${height}px` : '36px'
      ref.current.style.height = `${ref.current.scrollHeight}px`
    }
  }

  useEffect(() => adjustHeight(height), [value, height])

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    adjustHeight()
    if (onChange) onChange(e.target.value)
  }

  return (
    <textarea {...props} id={label} ref={ref} value={value} onChange={handleChange} className={clsx(style.line, className)} />
  )
}
