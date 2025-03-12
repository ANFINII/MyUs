import clsx from 'clsx'
import style from './Horizontal.module.scss'

interface Props {
  gap?: string | number
  align?: 'start' | 'center' | 'end' | 'around' | 'between' | 'evenly'
  wrap?: boolean
  full?: boolean
  className?: string
  children: React.ReactNode
}

export default function Horizontal(props: Props): JSX.Element {
  const { gap = 0, align, wrap, full, className, children } = props

  return (
    <div className={clsx(style.horizontal, style[`align_${align}`], full && style.full, className)} style={{ gap: `${Number(gap) * 2}px`, flexWrap: wrap ? 'wrap' : 'nowrap' }}>
      {children}
    </div>
  )
}
