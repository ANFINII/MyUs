import clsx from 'clsx'
import style from './VStack.module.scss'

interface Props {
  gap?: string
  align?: 'start' | 'center' | 'end' | 'baseline' | 'stretch'
  full?: boolean
  wrap?: boolean
  className?: string
  children: React.ReactNode
}

export default function VStack(props: Props): JSX.Element {
  const { gap = '0', align = 'stretch', full, wrap = false, className, children } = props

  return (
    <div className={clsx(style.vertical, style[align], full && style.full, wrap && style.wrap, className)} style={{ gap: `${Number(gap) * 2}px` }}>
      {children}
    </div>
  )
}
