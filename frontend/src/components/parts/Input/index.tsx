import style from 'components/parts/Input/Input.module.css'

interface Props {
  id?: string
  className?: string
  name?: string
  value?: string
  placeholder?: string
  required?: boolean
  disabled?: boolean
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void
}

export default function Input(props: Props) {
  const {id, className, name, value, placeholder, required, disabled, onChange} = props
  return (
    <>
      {required ?
        <input id={id} name={name} value={value} placeholder={placeholder} onChange={onChange} disabled={disabled} required
          className={`${style.input} ` + (className ? className : '' )}
        />
      :
        <input id={id} name={name} value={value} placeholder={placeholder} onChange={onChange} disabled={disabled}
          className={`${style.input} ` + (className ? className : '' )}
        />
      }
    </>
  )
}
