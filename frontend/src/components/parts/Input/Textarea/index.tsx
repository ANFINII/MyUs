import { useState, useRef, useEffect } from 'react'
import clsx from 'clsx'
import VStack from 'components/parts/Stack/Vertical'
import style from './Textarea.module.scss'

interface Props {
  label?: string
  errorText?: string
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
  onChange?: (e: React.ChangeEvent<HTMLTextAreaElement>) => void
}

export default function Textarea(props: Props): JSX.Element {
  const { label, errorText, value, className, height, error = false, required = false, focus, onChange } = props

  const ref = useRef<HTMLTextAreaElement>(null)
  const [isValue, setIsValue] = useState<boolean>(false)

  const isRequired = required && !isValue
  const isErrorText = !isRequired && error

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

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    adjustHeight()
    setIsValue(e.target.value !== '')
    onChange?.(e)
  }

  return (
    <VStack gap="2" className={className}>
      {label && (
        <label htmlFor={label} className={style.label}>
          {label}
        </label>
      )}
      <textarea {...props} id={label} ref={ref} value={value} onChange={handleChange} className={clsx(style.textarea, isRequired && style.error)} />
      {isRequired && <p className={style.error_text}>※必須入力です！</p>}
      {isErrorText && <p className={style.error_text}>{errorText}</p>}
    </VStack>
  )
}
