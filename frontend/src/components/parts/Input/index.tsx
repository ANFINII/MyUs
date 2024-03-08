import useAutoFocus from 'components/hooks/useAutoFocus'
import style from 'components/parts/Input/Input.module.scss'

interface Props {
  type?: string
  name?: string
  value?: string
  defaultValue?: string
  placeholder?: string
  id?: string
  className?: string
  minLength?: number
  maxLength?: number
  required?: boolean
  disabled?: boolean
  autoFocus?: boolean
  onChange?: (value: string) => void
  onClick?: (event: React.MouseEvent<HTMLInputElement>) => void
}

export default function Input(props: Props) {
  const { className, defaultValue = '', autoFocus, onChange } = props

  const inputFocus = useAutoFocus()
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => onChange && onChange(e.target.value)

  return <input {...props} defaultValue={defaultValue} onChange={handleChange} ref={autoFocus ? inputFocus : undefined} className={style.input + (className ? ' ' + className : '')} />
}
