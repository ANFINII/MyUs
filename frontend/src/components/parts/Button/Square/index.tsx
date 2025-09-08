import clsx from 'clsx'
import style from './Square.module.scss'

type ButtonColor = 'sakura' | 'emerald'

interface Props {
  name: string
  color?: ButtonColor
  type?: 'submit' | 'reset' | 'button'
  value?: string
  className?: string
  onClick?: () => void
}

export default function ButtonSquare(props: Props): React.JSX.Element {
  const { name, color = 'sakura', type = 'button', className = '' } = props

  return (
    <button {...props} type={type} className={clsx(style.button, style[color], className)}>
      {name}
    </button>
  )
}
