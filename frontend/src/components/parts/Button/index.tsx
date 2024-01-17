import style from 'components/parts/Button/Button3.module.scss'

interface Color {
  blue?: boolean
  purple?: boolean
  red?: boolean
  green?: boolean
}

interface Props extends Color {
  size?: 'xl' | 'xs'
  type?: 'submit' | 'reset' | 'button'
  name: string
  value?: string
  className?: string
  loading?: boolean
  disabled?: boolean
  onClick?(): void
}

export default function Button(props: Props): JSX.Element {
  const { blue, purple, red, green } = props
  const { size, type = 'button', name, value, className, loading, disabled, onClick } = props

  const colorCheck = (name: string, isColor?: boolean): string => {
    return isColor && !loading ? ' ' + style[name] : ''
  }

  const sizeCheck = (name: string): string => {
    return size === name ? ' ' + style[name] : ''
  }

  return (
    <button
      type={type}
      value={value}
      onClick={onClick}
      disabled={disabled || loading}
      className={
        style.button +
        colorCheck('blue', blue) +
        colorCheck('purple', purple) +
        colorCheck('red', red) +
        colorCheck('green', green) +
        sizeCheck('xl') +
        sizeCheck('xs') +
        (className ? ' ' + className : '')
      }
    >
      {loading && (
        <div className={style.spinner}>
          <i className="fa-regular fa-circle-notch"></i>
        </div>
      )}
      {!loading && name}
    </button>
  )
}
