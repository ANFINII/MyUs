import clsx from 'clsx'
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
  const { name, color = 'white', size = 'm', type = 'button', className = '', disabled = false, loading = false, icon } = props

  const spinnerColor = (color: string): SpinnerColor => {
    return color === 'white' ? 'gray' : 'white'
  }

  return (
    <button {...props} type={type} disabled={disabled || loading} className={clsx(style.button, style[color], style[size], className)}>
      <span className={style.flex}>
        {icon}
        {loading && <Spinner color={spinnerColor(color)} size="s" className={style.spinner} />}
        <span className={loading ? style.invisible : undefined}>{name}</span>
      </span>
    </button>
  )
}
