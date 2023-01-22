import style from 'components/parts/Input/Input.module.css'

interface Props {
  type?: "text" | "file"
  name?: string
  value?: string
  placeholder?: string
  id?: string
  className?: string
  accept?: string
  required?: boolean
  disabled?: boolean
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void
  onClick?: (event: React.MouseEventHandler<HTMLInputElement>) => void
}

export default function Input(props: Props) {
  const {type, name, value, placeholder, id, className, accept, required, disabled, onChange, onClick} = props
  return (
    <>
      {required ?
        <input type={type} name={name} value={value} placeholder={placeholder} onChange={onChange} onClick={onClick} disabled={disabled}
          id={id} className={`${style.input} ` + (className ? className : '' )} accept={accept} required
        />
      :
        <input type={type} name={name} value={value} placeholder={placeholder} onChange={onChange} onClick={onClick} disabled={disabled}
          id={id} className={`${style.input} ` + (className ? className : '' )} accept={accept}
        />
      }
    </>
  )
}
