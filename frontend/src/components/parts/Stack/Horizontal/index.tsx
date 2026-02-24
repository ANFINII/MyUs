import clsx from 'clsx'
import style from './Horizontal.module.scss'

interface Props {
  justify?: 'start' | 'center' | 'end' | 'around' | 'between' | 'evenly'
  align?: 'start' | 'center' | 'end' | 'baseline' | 'stretch'
  gap?: string
  full?: boolean
  wrap?: boolean
  className?: string
  children: React.ReactNode
}

export default function HStack(props: Props): React.JSX.Element {
  const { justify = 'start', align = 'center', gap = '0', full, wrap = false, className, children } = props

  return (
    <div className={clsx(style.horizontal, style[justify], style[`align_${align}`], full && style.full, wrap && style.wrap, className)} style={{ gap: `${Number(gap) * 2}px` }}>
      {children}
    </div>
  )
}
