import { Row } from 'types/internal/table'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'

interface Props {
  rows: Row[]
}

export default function TableList(props: Props) {
  const { rows } = props

  return (
    <Table>
      {rows.map((row) => (
        <TableRow key={row.label} label={row.label} isIndent={row.isIndent || true}>
          {row.content}
        </TableRow>
      ))}
    </Table>
  )
}
