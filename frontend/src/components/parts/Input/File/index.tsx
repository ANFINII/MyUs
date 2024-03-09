import { useRef, useState } from 'react'
import clsx from 'clsx'
import style from 'components/parts/Input/Input.module.scss'

interface Props {
  accept?: string
  onChange?: (file: File) => void
  required?: boolean
  className?: string
}

export default function InputFile(props: Props) {
  const { accept, onChange, required, className = '' } = props

  const inputEl = useRef<HTMLInputElement>(null)
  const [fileName, setFileName] = useState('')

  const handleClick = () => inputEl.current?.click()

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setFileName(file.name)
      onChange && onChange(file)
    }
  }

  return (
    <>
      <input ref={inputEl} type="file" accept={accept} onChange={handleChange} hidden />
      <input placeholder="ファイル選択..." value={fileName} required={required} onClick={handleClick} className={clsx(style.input, className)} />
    </>
  )
}
