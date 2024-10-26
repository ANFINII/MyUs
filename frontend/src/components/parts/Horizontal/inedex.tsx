import styles from './Horizontal.module.scss'

interface Props {
  gap?: string | number
  alignment?: 'start' | 'center' | 'end' | 'stretch'
  wrap?: boolean
  children: React.ReactNode
}

export default function Horizontal(props: Props): JSX.Element {
  const { gap, alignment, wrap, children } = props

  return (
    <div className={styles.horizontal} style={{ gap: `${Number(gap) * 2}px`, justifyContent: alignment, flexWrap: wrap ? 'wrap' : 'nowrap' }}>
      {children}
    </div>
  )
}
