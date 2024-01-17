import style from 'components/parts/Button/Square/Square.module.scss'

interface Color {
  emerald?: boolean
  red?: boolean
  sakura?: boolean
}

interface Props extends Color {
  type?: 'submit' | 'reset' | 'button'
  value?: string
  name?: string
  className?: string
  onClick?(): void
}

export default function ButtonSquare(props: Props) {
  const { emerald, sakura, red } = props
  const { type = 'button', value, name, className, onClick } = props

  const colorCheck = (isColor: boolean | undefined, name: string) => {
    return isColor ? ' ' + style[name] : ''
  }

  return (
    <button
      type={type}
      value={value}
      onClick={onClick}
      className={style.button + colorCheck(emerald, 'emerald') + colorCheck(sakura, 'sakura') + colorCheck(red, 'red') + (className ? ' ' + className : '')}
    >
      {name}
    </button>
  )
}
