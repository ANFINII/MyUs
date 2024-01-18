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
      <td className="td_color">{label}</td>
      <td className={isIndent ? 'td_indent' : ''}>{children}</td>
    </tr>
  )
}
