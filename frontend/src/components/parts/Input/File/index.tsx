import { ChangeEvent, useRef, useState } from 'react'
import cx from 'utils/functions/cx'
import style from '../Input.module.scss'

interface Props {
  label?: string
  accept?: string
  error?: string
  className?: string
  required?: boolean
  multiple?: boolean
  onChange?: (files: File | File[]) => void
}

export default function InputFile(props: Props): React.JSX.Element {
  const { label, accept, error, className, required = false, multiple, onChange } = props

  const inputEl = useRef<HTMLInputElement>(null)
  const [fileNames, setFileNames] = useState<string[]>([])

  const isError = !!error || (error === '' && required && fileNames.length === 0)

  const handleClick = () => inputEl.current?.click()

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      const names = Array.from(files).map((file) => file.name)
      setFileNames(names)
      const selectedFiles = multiple ? Array.from(files) : files[0]
      if (onChange && selectedFiles) onChange(selectedFiles)
    }
  }

  return (
    <div className={cx(style.box, className)}>
      {label && (
        <label htmlFor={label} className={style.label}>
          {label}
          {required && <span className={style.required}>*</span>}
        </label>
      )}
      <input id={label} ref={inputEl} type="file" accept={accept} onChange={handleChange} multiple={multiple} hidden />
      <input placeholder="ファイル選択..." value={fileNames.join(', ')} required={required} onClick={handleClick} className={cx(style.input, isError && style.error)} />
      {error && <p className={style.error_text}>{error}</p>}
    </div>
  )
}
