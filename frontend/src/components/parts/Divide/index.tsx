import clsx from 'clsx'
import style from './Divide.module.scss'

interface Props {
  margin?: 'mv_4' | 'mv_8' | 'mv_16' | 'mv_20' | 'mv_24'
  className?: string
}

export default function Divide(props: Props): JSX.Element {
  const { margin = 'mv_16', className } = props
  return <hr className={clsx(style.hr, margin, className)} />
}
