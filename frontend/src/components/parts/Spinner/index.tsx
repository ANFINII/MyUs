import style from 'components/parts/Spinner/Spinner.module.scss'

interface Color {
  blue?: boolean
  purple?: boolean
  red?: boolean
  green?: boolean
}

interface Props extends Color {
  size?: 's' | 'm' | 'l'
  className?: string
}

export default function Spinner(props: Props): JSX.Element {
  const { blue, purple, red, green, size = 'm', className } = props

  const colorCheck = (name: string, isColor?: boolean): string => {
    return isColor ? ' ' + style[name] : ''
  }

  const sizeCheck = (name: string): string => {
    return size === name ? ' ' + style[name] : ''
  }

  return (
    <span
      className={
        style.spinner +
        colorCheck('blue', blue) +
        colorCheck('purple', purple) +
        colorCheck('red', red) +
        colorCheck('green', green) +
        sizeCheck('s') +
        sizeCheck('m') +
        sizeCheck('l') +
        (className ? ' ' + className : '')
      }
    ></span>
  )
}
