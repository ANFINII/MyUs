import { ChangeEvent, KeyboardEvent, useEffect, useRef } from 'react'
import clsx from 'clsx'
import style from './Line.module.scss'

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
  focus?: boolean
  onChange?: (e: ChangeEvent<HTMLTextAreaElement>) => void
  onSubmit?: () => void
}

export default function TextareaLine(props: Props): React.JSX.Element {
  const { label, value, className, height, focus, onChange, onSubmit } = props

  const ref = useRef<HTMLTextAreaElement>(null)

  const adjustHeight = (height?: number) => {
    if (ref?.current) {
      ref.current.style.height = height ? `${height}px` : '36px'
      ref.current.style.height = `${ref.current.scrollHeight}px`
    }
  }

  useEffect(() => adjustHeight(height), [value, height])

  useEffect(() => {
    if (focus && ref.current) ref.current.focus()
  }, [focus])

  const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
    adjustHeight()
    onChange?.(e)
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      e.preventDefault()
      onSubmit?.()
    }
  }

  return <textarea {...props} id={label} ref={ref} value={value} onChange={handleChange} onKeyDown={handleKeyDown} className={clsx(style.line, className)} />
}
