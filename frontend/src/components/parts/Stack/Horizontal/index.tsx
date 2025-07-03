import clsx from 'clsx'
import style from './Horizontal.module.scss'

interface Props {
  gap?: string
  justify?: 'start' | 'center' | 'end' | 'around' | 'between' | 'evenly'
  full?: boolean
  wrap?: boolean
  className?: string
  children: React.ReactNode
}

export default function HStack(props: Props): JSX.Element {
  const { gap = '0', justify = 'start', full, wrap = false, className, children } = props

  return (
    <div className={clsx(style.horizontal, style[justify], full && style.full, wrap && style.wrap, className)} style={{ gap: `${Number(gap) * 2}px` }}>
      {children}
    </div>
  )
}
