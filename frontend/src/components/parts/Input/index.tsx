import style from 'components/parts/Input/Input.module.css'

interface Props {
  name?: string
  value?: string
  placeholder?: string
  id?: string
  className?: string
  required?: boolean
  disabled?: boolean
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void
  onClick?: (event: React.MouseEvent<HTMLInputElement>) => void
}

export default function Input(props: Props) {
  const {name, value, placeholder, id, className, required, disabled, onChange, onClick} = props
  return (
    <>
      {required ?
        <input name={name} value={value} placeholder={placeholder} disabled={disabled} onChange={onChange} onClick={onClick}
          id={id} className={`${style.input} ` + (className ? className : '' )} required
        />
      :
        <input name={name} value={value} placeholder={placeholder} disabled={disabled} onChange={onChange} onClick={onClick}
          id={id} className={`${style.input} ` + (className ? className : '' )}
        />
      }
    </>
  )
}
