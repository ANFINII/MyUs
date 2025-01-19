import clsx from 'clsx'
import style from './Vertical.module.scss'

interface Props {
  gap?: string | number
  align?: 'start' | 'center' | 'end' | 'around' | 'between' | 'evenly'
  className?: string
  children: React.ReactNode
}

export default function Vertical(props: Props): JSX.Element {
  const { gap = 0, align, className, children } = props

  return (
    <div className={clsx(style.vertical, style[`align_${align}`], className)} style={{ gap: `${Number(gap) * 2}px`, alignItems: align }}>
      {children}
    </div>
  )
}
