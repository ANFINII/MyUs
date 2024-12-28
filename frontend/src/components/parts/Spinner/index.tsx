import clsx from 'clsx'
import style from './Spinner.module.scss'

export type SpinnerColor = 'white' | 'gray' | 'blue'

interface Props {
  color?: SpinnerColor
  size?: 's' | 'm' | 'l'
  className?: string
}

export default function Spinner(props: Props) {
  const { color = 'white', size = 'm', className = '' } = props

  return <span className={clsx(style.spinner, style[color], style[size], className)}></span>
}
