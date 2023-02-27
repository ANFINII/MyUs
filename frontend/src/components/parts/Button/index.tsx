import style from 'components/parts/Button/Button.module.css'

interface Color {
  blue?: boolean
  purple?: boolean
  red?: boolean
  green?: boolean
  light?: boolean
}

interface Props extends Color {
  size?: 'xl' | 'xs'
  type?: 'submit' | 'reset' | 'button'
  value?: string
  className?: string
  children?: string | string[]
  onClick?(): void
}

export default function Button(props: Props) {
  const {blue, purple, red, green, light} = props
  const {size, type, value, className, children, onClick} = props

  return (
    <button type={type} value={value} onClick={onClick}
      className={
        `${style.button} `
        + (blue ? `${style.blue} ` : '')
        + (purple ? `${style.purple} ` : '')
        + (red ? `${style.red} ` : '')
        + (green ? `${style.green} ` : '')
        + (light ? `${style.light} ` : '')
        + (size === 'xl' ? `${style.xl} ` : '')
        + (size === 'xs' ? `${style.xs} ` : '')
        + (className ? className : '' )
      }
    >{children}
    </button>
  )
}