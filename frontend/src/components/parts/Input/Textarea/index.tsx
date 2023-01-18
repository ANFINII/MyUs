import {useState} from 'react'
import style from 'components/parts/Input/Textarea/Textarea.module.css'

interface Props {
  id?: string
  className?: string
  name?: string
  value?: string
  placeholder?: string
  required?: boolean
  disabled?: boolean
}

export default function Textarea(props: Props) {
  const {id, className, name, value, placeholder, required, disabled} = props

  const [rows, serRows] = useState(1)
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const height = e.target.value.split('\n').length
    serRows(height)
  }

  return (
    <>
      {required ?
        <textarea id={id} name={name} value={value} placeholder={placeholder}
          rows={rows} onChange={handleChange} disabled={disabled} required
          className={`${style.textarea} ` + (className ? className : '' )}
        >
        </textarea>
      :
        <textarea id={id} name={name} value={value} placeholder={placeholder}
          rows={rows} onChange={handleChange} disabled={disabled}
          className={`${style.textarea} ` + (className ? className : '' )}
        >
        </textarea>
      }
    </>
  )
}
