import clsx from 'clsx'
import Spinner from 'components/parts/Spinner'
import { SpinnerColor } from 'components/parts/Spinner'
import style from 'components/parts/Button/Button.module.scss'

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
}

export default function Button(props: Props): JSX.Element {
  const { name, color = 'white', size = 'm', type = 'button', className = '', disabled = false, loading = false } = props

  const spinnerColor = (color: string): SpinnerColor => {
    return color === 'white' ? 'gray' : 'white'
  }

  return (
    <button {...props} type={type} disabled={disabled || loading} className={clsx(style.button, style[color], style[size], className)}>
      {loading && <Spinner color={spinnerColor(color)} size="s" className={style.spinner} />}
      {loading ? <span className={style.loading}>{name}</span> : name}
    </button>
  )
}
