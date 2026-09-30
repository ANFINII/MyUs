import cx from 'utils/functions/cx'
import style from './Vertical.module.scss'

type StackGap = '0' | '0.5' | '1' | '2' | '2.5' | '3' | '4' | '5' | '6' | '8' | '10' | '12'

interface Props {
  align?: 'start' | 'center' | 'end' | 'baseline' | 'stretch'
  gap?: StackGap
  full?: boolean
  wrap?: boolean
  className?: string
  children: React.ReactNode
}

export default function VStack(props: Props): React.JSX.Element {
  const { align = 'stretch', gap = '0', full, wrap = false, className, children } = props

  return (
    <div className={cx(style.vertical, style[align], full && style.full, wrap && style.wrap, style[`gap_${gap.replace('.', '_')}`], className)}>
      {children}
    </div>
  )
}
