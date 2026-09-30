import cx from 'utils/functions/cx'
import Spinner, { SpinnerColor } from 'components/parts/Spinner'
import style from './Button.module.scss'

type ButtonColor = 'white' | 'black' | 'blue' | 'purple' | 'red' | 'green' | 'mono'

interface Props {
  name: string
  color?: ButtonColor
  size?: 's' | 'm' | 'l'
  type?: 'submit' | 'reset' | 'button'
  value?: string
  className?: string
  disabled?: boolean
  loading?: boolean
  onClick?: () => void
  icon?: React.ReactNode
}

export default function Button(props: Props): React.JSX.Element {
  const { name, color = 'white', size = 'm', type = 'button', value, className, disabled = false, loading = false, onClick, icon } = props

  const spinnerColor: SpinnerColor = color === 'white' ? 'gray' : 'white'

  return (
    <button name={name} type={type} value={value} disabled={disabled || loading} onClick={onClick} className={cx(style.button, style[color], style[size], className)}>
      <span className={style.flex}>
        {icon}
        {loading && <Spinner color={spinnerColor} size="s" className={style.spinner} />}
        <span className={loading ? style.invisible : undefined}>{name}</span>
      </span>
    </button>
  )
}
