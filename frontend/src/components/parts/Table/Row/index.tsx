import clsx from 'clsx'
import style from '../Table.module.scss'

interface Props {
  label: string
  className?: string
  isIndent?: boolean
  children: React.ReactNode
}

export default function TableRow(props: Props): React.JSX.Element {
  const { label, className, isIndent, children } = props

  return (
    <tr className={className}>
      <td className={style.label}>{label}</td>
      <td className={clsx(isIndent && style.indent)}>{children}</td>
    </tr>
  )
}
