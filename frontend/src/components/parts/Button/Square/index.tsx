import cx from 'utils/functions/cx'
import Spinner, { SpinnerColor } from 'components/parts/Spinner'
import style from './Square.module.scss'

type ButtonColor = 'sakura' | 'emerald'

interface Props {
  name: string
  color?: ButtonColor
  type?: 'submit' | 'reset' | 'button'
  value?: string
  className?: string
  disabled?: boolean
  loading?: boolean
  onClick?: () => void
}

export default function ButtonSquare(props: Props): React.JSX.Element {
  const { name, color = 'sakura', type = 'button', className = '', disabled = false, loading = false } = props

  const spinnerColor = (color: string): SpinnerColor => {
    return color === 'sakura' ? 'white' : 'white'
  }

  return (
    <button {...props} type={type} disabled={disabled || loading} className={cx(style.button, style[color], className)}>
      <span className={style.flex}>
        {loading && <Spinner color={spinnerColor(color)} size="s" className={style.spinner} />}
        <span className={loading ? style.invisible : undefined}>{name}</span>
      </span>
    </button>
  )
}
