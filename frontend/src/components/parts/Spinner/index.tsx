import clsx from 'clsx'
import style from 'components/parts/Spinner/Spinner.module.scss'

export type SpinnerColor = 'white' | 'gray' | 'blue'

interface Props {
  color?: SpinnerColor
  size?: 's' | 'm' | 'l'
  className?: string
}

export default function Spinner(props: Props): JSX.Element {
  const { color = 'white', size = 'm', className } = props

  return <span className={clsx(style.spinner, style[color], style[size], className ? className : '')}></span>
}
