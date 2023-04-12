import style from 'components/parts/Input/Input.module.css'
import useAutoFocus from 'components/hooks/useAutoFocus'

interface Props {
  type?: string
  name?: string
  value?: string
  placeholder?: string
  id?: string
  className?: string
  minLength?: number
  maxLength?: number
  required?: boolean
  disabled?: boolean
  autoFocus?: boolean
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void
  onClick?: (event: React.MouseEvent<HTMLInputElement>) => void
}

export default function Input(props: Props) {
  const {type, name, value, placeholder, id, className, onChange, onClick} = props
  const {minLength, maxLength, required, disabled, autoFocus} = props
  const inputFocus = useAutoFocus()

  return (
    <input type={type} name={name} value={value} placeholder={placeholder}
      minLength={minLength} maxLength={maxLength} required={required} disabled={disabled}
      onChange={onChange} onClick={onClick} ref={autoFocus ? inputFocus : undefined}
      id={id} className={style.input + (className ? ' ' + className : '')}
    />
  )
}
