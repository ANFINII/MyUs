import clsx from 'utils/functions/clsx'
import style from './Card.module.scss'

interface Props {
  className?: string
  children: React.ReactNode
}

export default function Card(props: Props): React.JSX.Element {
  const { className, children } = props

  return <section className={clsx(style.card, className)}>{children}</section>
}
