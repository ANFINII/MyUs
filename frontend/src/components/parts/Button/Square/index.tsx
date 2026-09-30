import cx from 'utils/functions/cx'
import Spinner from 'components/parts/Spinner'
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
  const { name, color = 'sakura', type = 'button', value, className, disabled = false, loading = false, onClick } = props

  return (
    <button name={name} type={type} value={value} disabled={disabled || loading} onClick={onClick} className={cx(style.button, style[color], className)}>
      <span className={style.flex}>
        {loading && <Spinner color="white" size="s" className={style.spinner} />}
        <span className={loading ? style.invisible : undefined}>{name}</span>
      </span>
    </button>
  )
}
