import styles from './Vertical.module.scss'

interface Props {
  gap?: string | number
  alignment?: 'start' | 'center' | 'end' | 'stretch'
  children: React.ReactNode
}

export default function Vertical(props: Props): JSX.Element {
  const { gap, alignment, children } = props

  return (
    <div className={styles.vertical} style={{ gap: `${Number(gap) * 2}px`, alignItems: alignment }}>
      {children}
    </div>
  )
}
