import { ChangeEvent, useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import cx from 'utils/functions/cx'
import style from '../Input.module.scss'

interface Props {
  label?: string
  accept?: string
  error?: string
  className?: string
  required?: boolean
  onChange?: (file: File) => void
  onMultiChange?: (files: File[]) => void
}

export default function InputFile(props: Props): React.JSX.Element {
  const { label, accept, error, className, required = false, onChange, onMultiChange } = props

  const { t } = useTranslation()
  const inputEl = useRef<HTMLInputElement>(null)
  const [fileNames, setFileNames] = useState<string[]>([])

  const isMultiple = onMultiChange !== undefined
  const isError = !!error || (error === '' && required && fileNames.length === 0)

  const handleClick = () => inputEl.current?.click()

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (!files || files.length === 0) return
    const selectedFiles = Array.from(files)
    setFileNames(selectedFiles.map((file) => file.name))
    if (isMultiple) return onMultiChange(selectedFiles)
    if (onChange && selectedFiles[0]) onChange(selectedFiles[0])
  }

  return (
    <div className={cx(style.box, className)}>
      {label && (
        <label htmlFor={label} className={style.label}>
          {label}
          {required && <span className={style.required}>*</span>}
        </label>
      )}
      <input id={label} ref={inputEl} type="file" accept={accept} onChange={handleChange} multiple={isMultiple} hidden />
      <input placeholder={t('input.file')} value={fileNames.join(', ')} required={required} onClick={handleClick} className={cx(style.input, isError && style.error)} />
      {error && <p className={style.error_text}>{error}</p>}
    </div>
  )
}
