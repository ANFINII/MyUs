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
  value?: string
  className?: string
  disabled?: boolean
  children?: string | string[]
  onClick?(): void
}

export default function Button(props: Props) {
  const {blue, purple, red, green} = props
  const {size, type, value, className, disabled, children, onClick} = props

  const colorCheck = (isColor: boolean | undefined, name: string) => {
    return isColor ? ' ' + style[name] : ''
  }

  const sizeCheck = (name: string) => {
    return size ===  name ? ' ' + style[name] : ''
  }

  return (
    <button type={type} value={value} onClick={onClick} disabled={disabled}
      className={
        style.button +
        colorCheck(blue, 'blue') +
        colorCheck(purple, 'purple') +
        colorCheck(red, 'red') +
        colorCheck(green, 'green') +
        sizeCheck('xl') +
        sizeCheck('xs') +
        (className ? ' ' + className : '')
      }
    >{children}
    </button>
  )
}
