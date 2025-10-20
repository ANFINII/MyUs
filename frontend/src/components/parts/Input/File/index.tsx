import { ChangeEvent, useRef, useState } from 'react'
import clsx from 'clsx'
import VStack from 'components/parts/Stack/Vertical'
import style from '../Input.module.scss'

interface Props {
  label?: string
  errorText?: string
  accept?: string
  className?: string
  error?: boolean
  required?: boolean
  multiple?: boolean
  onChange?: (files: File | File[]) => void
}

export default function InputFile(props: Props): React.JSX.Element {
  const { label, errorText, accept, className, error = false, required = false, multiple, onChange } = props

  const inputEl = useRef<HTMLInputElement>(null)
  const [fileNames, setFileNames] = useState<string[]>([])

  const isRequired = required && fileNames.length === 0
  const isErrorText = !isRequired && error

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
    <VStack gap="2" className={className}>
      {label && (
        <label htmlFor={label} className={style.label}>
          {label}
        </label>
      )}
      <input id={label} ref={inputEl} type="file" accept={accept} onChange={handleChange} multiple={multiple} hidden />
      <input placeholder="ファイル選択..." value={fileNames.join(', ')} required={required} onClick={handleClick} className={clsx(style.input, isRequired && style.error)} />
      {isRequired && <p className={style.error_text}>※必須入力です！</p>}
      {isErrorText && <p className={style.error_text}>{errorText}</p>}
    </VStack>
  )
}
