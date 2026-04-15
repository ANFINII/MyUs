import { useMemo, useState } from 'react'
import cx from 'utils/functions/cx'
import style from './DataTable.module.scss'

export interface Column<T> {
  key: string
  header: string
  sortable?: boolean
  sortValue?: (row: T) => string | number
  render: (row: T) => React.ReactNode
  className?: string
  cellClassName?: string
}

interface Props<T> {
  datas: T[]
  columns: Column<T>[]
  rowKey: (row: T) => string
}

type SortOrder = 'asc' | 'desc'

export default function DataTable<T>(props: Props<T>): React.JSX.Element {
  const { datas, columns, rowKey } = props

  const [sortKey, setSortKey] = useState<string | null>(null)
  const [sortOrder, setSortOrder] = useState<SortOrder>('asc')

  const handleSort = (key: string) => {
    if (sortKey === key) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')
      return
    }
    setSortKey(key)
    setSortOrder('desc')
  }

  const sortedDatas = useMemo(() => {
    if (sortKey === null) return datas
    const column = columns.find((c) => c.key === sortKey)
    if (!column || !column.sortValue) return datas
    const sortValue = column.sortValue
    const copied = [...datas]
    copied.sort((a, b) => {
      const va = sortValue(a)
      const vb = sortValue(b)
      if (va < vb) return sortOrder === 'asc' ? -1 : 1
      if (va > vb) return sortOrder === 'asc' ? 1 : -1
      return 0
    })
    return copied
  }, [datas, columns, sortKey, sortOrder])

  const sortMark = (key: string): string => {
    if (sortKey !== key) return ''
    return sortOrder === 'asc' ? '↑' : '↓'
  }

  return (
    <div className={style.table_wrap}>
      <table className={style.table}>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.key} className={column.className}>
                {column.sortable ? (
                  <button type="button" className={style.sort_button} onClick={() => handleSort(column.key)}>
                    {column.header}
                    <span className={style.sort_mark}>{sortMark(column.key)}</span>
                  </button>
                ) : (
                  column.header
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sortedDatas.map((row) => (
            <tr key={rowKey(row)}>
              {columns.map((column) => (
                <td key={column.key} className={cx(column.className, column.cellClassName)}>
                  {column.render(row)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      {datas.length === 0 && <div className={style.empty}>データがありません</div>}
    </div>
  )
}
