import style from 'components/parts/Button/Square/Square.module.css'

interface Color {
  emerald?: boolean
  red?: boolean
  sakura?: boolean
}

interface Props extends Color {
  type?: 'submit' | 'reset' | 'button'
  value?: string
  className?: string
  children?: string | string[]
  onClick?(): void
}

export default function ButtonSquare(props: Props) {
  const {emerald, sakura, red} = props
  const {type, value, className, children, onClick} = props

  return (
    <button type={type} value={value} onClick={onClick}
      className={
        `${style.button} `
        + (emerald ? `${style.emerald} ` : '')
        + (sakura ? `${style.sakura} ` : '')
        + (red ? `${style.red} ` : '')
        + (className ? className : '')
      }
    >{children}
    </button>
  )
}
