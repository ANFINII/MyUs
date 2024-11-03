import clsx from 'clsx'
import styles from './Horizontal.module.scss'

interface Props {
  gap?: string | number
  alignment?: 'start' | 'center' | 'end' | 'stretch'
  wrap?: boolean
  className?: string
  children: React.ReactNode
}

export default function Horizontal(props: Props): JSX.Element {
  const { gap, alignment, wrap, className, children } = props

  return (
    <div className={clsx(styles.horizontal, className)} style={{ gap: `${Number(gap) * 2}px`, justifyContent: alignment, flexWrap: wrap ? 'wrap' : 'nowrap' }}>
      {children}
    </div>
  )
}
