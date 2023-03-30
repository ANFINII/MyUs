import {useState, useRef} from 'react'
import style from 'components/parts/Input/Input.module.css'

interface Props {
  id?: string
  className?: string
  accept?: string
  required?: boolean
}

export default function InputFile(props: Props) {
  const {id, className, accept, required} = props
  const inputEl = useRef<HTMLInputElement>(null)
  const [fileName, setFileName] = useState('')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFileName(e.target.value.replace('C:\\fakepath\\', ''))
  }
  const handleClick = () => inputEl.current?.click()

  return (
    <>
      <input type="file" id={id} accept={accept} ref={inputEl} onChange={handleChange} hidden />
      <input placeholder="ファイル選択..." value={fileName} required={required} onClick={handleClick}
        className={`${style.input} ` + (className ? className : '')}
      />
    </>
  )
}
