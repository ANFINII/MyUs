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
      <td className={style.td_color}>{label}</td>
      <td className={isIndent ? style.td_indent : style.td_no}>{children}</td>
    </tr>
  )
}
