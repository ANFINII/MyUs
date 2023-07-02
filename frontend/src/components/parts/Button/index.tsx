import style from 'components/parts/Button/Button.module.css'

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
  disabled?: boolean
  onClick?(): void
}

export default function Button(props: Props): JSX.Element {
  const { blue, purple, red, green } = props
  const { size, type, name, value, className, disabled, onClick } = props

  const colorCheck = (name: string, isColor?: boolean): string => {
    return isColor ? ' ' + style[name] : ''
  }

  const sizeCheck = (name: string): string => {
    return size === name ? ' ' + style[name] : ''
  }

  return (
    <button type={type} value={value} onClick={onClick} disabled={disabled}
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
      {name}
    </button>
  )
}
