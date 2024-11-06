import clsx from 'clsx'
import style from './Horizontal.module.scss'

interface Props {
  gap?: string | number
  align?: 'start' | 'center' | 'end' | 'stretch'
  wrap?: boolean
  className?: string
  children: React.ReactNode
}

export default function Horizontal(props: Props): JSX.Element {
  const { gap = 0, align, wrap, className, children } = props

  return (
    <div className={clsx(style.horizontal, className)} style={{ gap: `${Number(gap) * 2}px`, justifyContent: align, flexWrap: wrap ? 'wrap' : 'nowrap' }}>
      {children}
    </div>
  )
}
