import clsx from 'clsx'
import style from './Vertical.module.scss'

interface Props {
  align?: 'start' | 'center' | 'end' | 'baseline' | 'stretch'
  gap?: string
  full?: boolean
  wrap?: boolean
  className?: string
  children: React.ReactNode
}

export default function VStack(props: Props): React.JSX.Element {
  const { align = 'stretch', gap = '0', full, wrap = false, className, children } = props

  return (
    <div className={clsx(style.vertical, style[align], full && style.full, wrap && style.wrap, className)} style={{ gap: `${Number(gap) * 2}px` }}>
      {children}
    </div>
  )
}
