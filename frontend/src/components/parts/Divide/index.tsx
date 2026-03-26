import clsx from 'clsx'
import style from './Divide.module.scss'

interface Props {
  label?: string
  position?: 'left' | 'center'
  height?: 'thin' | 'normal'
  marginV?: 'mv_0' | 'mv_4' | 'mv_8' | 'mv_16' | 'mv_20' | 'mv_24'
  marginH?: 'mh_0' | 'mh_4' | 'mh_8' | 'mh_12' | 'mh_16'
  className?: string
}

export default function Divide(props: Props): React.JSX.Element {
  const { label, position = 'center', height = 'normal', marginV = 'mv_16', marginH = 'mh_0', className } = props

  if (label) {
    return (
      <div className={clsx(style.labeled, style[marginV], style[marginH], className)}>
        {position === 'center' && <span className={clsx(style.line, style[height])} />}
        <span className={style.label}>{label}</span>
        <span className={clsx(style.line, style[height])} />
      </div>
    )
  }

  return <hr className={clsx(style.hr, style[height], style[marginV], style[marginH], className)} />
}
