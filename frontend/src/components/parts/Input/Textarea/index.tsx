import { ChangeEvent, useState, useRef, useEffect } from 'react'
import cx from 'utils/functions/cx'
import style from './Textarea.module.scss'

interface Props {
  label?: string
  value?: string
  name?: string
  defaultValue?: string
  placeholder?: string
  error?: string
  className?: string
  height?: number
  required?: boolean
  disabled?: boolean
  focus?: boolean
  onChange?: (e: ChangeEvent<HTMLTextAreaElement>) => void
}

export default function Textarea(props: Props): React.JSX.Element {
  const { label, value, error, className, height, required = false, focus, onChange, ...rest } = props

  const ref = useRef<HTMLTextAreaElement>(null)
  const [isValue, setIsValue] = useState<boolean>(false)

  const isError = !!error || (error === '' && required && !isValue && !value)

  const adjustHeight = (height?: number) => {
    if (ref.current) {
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
    setIsValue(e.target.value !== '')
    onChange?.(e)
  }

  return (
    <div className={cx(style.box, className)}>
      {label && (
        <label htmlFor={label} className={style.label}>
          {label}
          {required && <span className={style.required}>*</span>}
        </label>
      )}
      <textarea {...rest} id={label} ref={ref} value={value} required={required} onChange={handleChange} className={cx(style.textarea, isError && style.error)} />
      {error && <p className={style.error_text}>{error}</p>}
    </div>
  )
}
