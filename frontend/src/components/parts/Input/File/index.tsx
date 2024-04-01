import { useRef, useState } from 'react'
import clsx from 'clsx'
import style from 'components/parts/Input/Input.module.scss'

interface Props {
  label?: string
  errorText?: string
  accept?: string
  className?: string
  error?: boolean
  required?: boolean
  onChange?: (file: File) => void
}

export default function InputFile(props: Props) {
  const { label, errorText, accept, className = '', error = false, required = false, onChange } = props

  const inputEl = useRef<HTMLInputElement>(null)
  const [fileName, setFileName] = useState('')

  const isRequired = required && !fileName
  const isErrorText = !isRequired && error

  const handleClick = () => inputEl.current?.click()

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setFileName(file.name)
      onChange && onChange(file)
    }
  }

  return (
    <div className={className}>
      {label && (
        <label htmlFor={label} className={style.label}>
          {label}
        </label>
      )}
      <input id={label} ref={inputEl} type="file" accept={accept} onChange={handleChange} hidden />
      <input placeholder="ファイル選択..." value={fileName} required={required} onClick={handleClick} className={clsx(style.input, isRequired && style.error)} />
      {isRequired && <p className={style.error_text}>※必須入力です！</p>}
      {isErrorText && <p className={style.error_text}>{errorText}</p>}
    </div>
  )
}
