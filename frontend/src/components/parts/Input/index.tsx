import useAutoFocus from 'components/hooks/useAutoFocus'
import style from 'components/parts/Input/Input.module.scss'

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
  const { className, autoFocus } = props
  const inputFocus = useAutoFocus()

  return <input {...props} ref={autoFocus ? inputFocus : undefined} className={style.input + (className ? ' ' + className : '')} />
}
