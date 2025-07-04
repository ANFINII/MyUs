import { useRef, useEffect } from 'react'
import clsx from 'clsx'
import style from './TextareaLine.module.scss'

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
  onChange?: (e: React.ChangeEvent<HTMLTextAreaElement>) => void
}

export default function TextareaLine(props: Props): JSX.Element {
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
    onChange?.(e)
  }

  return <textarea {...props} id={label} ref={ref} value={value} onChange={handleChange} className={clsx(style.line, className)} />
}
