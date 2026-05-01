import DataTable, { Column } from 'components/parts/DataTable'
import Pagination from 'components/parts/Pagination'
import DeleteModal from 'components/widgets/Modal/Delete'
import style from './List.module.scss'

interface Props<T> {
  table: {
    datas: T[]
    columns: Column<T>[]
    rowKey: (row: T) => string
  }
  selection: {
    keys: Set<string>
    onChange: (keys: Set<string>) => void
  }
  pagination: {
    current: number
    total: number
    onChange: (page: number) => void
  }
  deletion: {
    label: string
    open: boolean
    loading: boolean
    onClose: () => void
    onAction: () => void
  }
}

export default function ManageList<T>(props: Props<T>): React.JSX.Element {
  const { table, selection, pagination, deletion } = props

  return (
    <>
      <div className={style.manage}>
        <DataTable
          datas={table.datas}
          columns={table.columns}
          rowKey={table.rowKey}
          selectable
          selectedKeys={selection.keys}
          onSelection={selection.onChange}
          footer={<Pagination currentPage={pagination.current} totalPages={pagination.total} onChange={pagination.onChange} />}
        />
      </div>
      <DeleteModal
        open={deletion.open}
        title={`${deletion.label}の削除`}
        content={`${selection.keys.size}件の${deletion.label}を削除しますか？`}
        loading={deletion.loading}
        onClose={deletion.onClose}
        onAction={deletion.onAction}
      />
    </>
  )
}
