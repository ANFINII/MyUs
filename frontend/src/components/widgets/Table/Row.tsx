import style from 'components/widgets/Table/Table.module.scss'

interface Props {
  label: string
  className?: string
  isIndent?: boolean
  children: React.ReactNode
}

export default function TableRow(props: Props) {
  const { label, className, isIndent, children } = props

  return (
    <tr className={className}>
      <td className={style.td_color}>{label}</td>
      <td className={isIndent ? style.td_indent : undefined}>{children}</td>
    </tr>
  )
}
