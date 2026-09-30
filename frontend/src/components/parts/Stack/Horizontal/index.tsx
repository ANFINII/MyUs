import cx from 'utils/functions/cx'
import style from './Horizontal.module.scss'

type StackGap = '0' | '0.5' | '1' | '2' | '2.5' | '3' | '4' | '5' | '6' | '8' | '10' | '12'

interface Props {
  justify?: 'start' | 'center' | 'end' | 'around' | 'between' | 'evenly'
  align?: 'start' | 'center' | 'end' | 'baseline' | 'stretch'
  gap?: StackGap
  full?: boolean
  wrap?: boolean
  className?: string
  children: React.ReactNode
}

export default function HStack(props: Props): React.JSX.Element {
  const { justify = 'start', align = 'center', gap = '0', full, wrap = false, className, children } = props

  return (
    <div className={cx(style.horizontal, style[justify], style[`align_${align}`], full && style.full, wrap && style.wrap, style[`gap_${gap.replace('.', '_')}`], className)}>
      {children}
    </div>
  )
}
