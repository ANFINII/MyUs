import clsx from 'clsx'
import style from './Horizontal.module.scss'

interface Props {
  gap?: string
  justify?: 'start' | 'center' | 'end' | 'around' | 'between' | 'evenly'
  wrap?: boolean
  full?: boolean
  className?: string
  children: React.ReactNode
}

export default function Horizontal(props: Props): JSX.Element {
  const { gap = '0', justify = 'start', wrap = false, full, className, children } = props

  return (
    <div className={clsx(style.horizontal, style[`justify_${justify}`], wrap && style.wrap, full && style.full, className)} style={{ gap: `${Number(gap) * 2}px` }}>
      {children}
    </div>
  )
}
