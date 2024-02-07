import { useRef, useState } from 'react'
import style from 'components/parts/Input/Input.module.scss'

interface Props {
  id?: string
  accept?: string
  onChange?: (file: File) => void
  required?: boolean
  className?: string
}

export default function InputFile(props: Props) {
  const { id, accept, onChange, required, className } = props

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
      <input ref={inputEl} type="file" id={id} accept={accept} onChange={handleChange} hidden />
      <input placeholder="ファイル選択..." value={fileName} required={required} onClick={handleClick} className={style.input + (className ? ' ' + className : '')} />
    </>
  )
}
