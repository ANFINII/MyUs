import clsx from 'clsx'
import styles from './Vertical.module.scss'

interface Props {
  gap?: string | number
  alignment?: 'start' | 'center' | 'end' | 'stretch'
  className?: string
  children: React.ReactNode
}

export default function Vertical(props: Props): JSX.Element {
  const { gap, alignment, className, children } = props

  return (
    <div className={clsx(styles.vertical, className)} style={{ gap: `${Number(gap) * 2}px`, alignItems: alignment }}>
      {children}
    </div>
  )
}
