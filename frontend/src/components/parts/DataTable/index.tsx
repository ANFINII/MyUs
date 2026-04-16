import { useState } from 'react'
import cx from 'utils/functions/cx'
import style from './DataTable.module.scss'

type SortOrder = 'asc' | 'desc'

export interface Column<T> {
  key: string
  header: string
  align?: 'left' | 'center' | 'right'
  sortable?: boolean
  sortValue?: (row: T) => string | number
  cell: (row: T) => React.ReactNode
  className?: string
  headerClass?: string
  cellClass?: string
}

interface Props<T> {
  datas: T[]
  columns: Column<T>[]
  rowKey: (row: T) => string
  selectable?: boolean
  selectedKeys?: Set<string>
  onSelection?: (selectedKeys: Set<string>) => void
  footer?: React.ReactNode
}

export default function DataTable<T>(props: Props<T>): React.JSX.Element {
  const { datas, columns, rowKey, selectable, selectedKeys, onSelection, footer } = props

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

  const sortedDatas = (() => {
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
  })()

  const sortMark = (key: string): string => {
    if (sortKey !== key) return ''
    return sortOrder === 'asc' ? '↑' : '↓'
  }

  const isAllSelected = datas.length > 0 && selectedKeys?.size === datas.length

  const handleSelectAll = () => {
    if (!onSelection) return
    if (isAllSelected) {
      onSelection(new Set())
      return
    }
    onSelection(new Set(datas.map((row) => rowKey(row))))
  }

  const handleSelectRow = (key: string) => {
    if (!onSelection || !selectedKeys) return
    const next = new Set(selectedKeys)
    if (next.has(key)) {
      next.delete(key)
    } else {
      next.add(key)
    }
    onSelection(next)
  }

  return (
    <div className={style.data_table}>
      <table className={style.table}>
        <thead className={style.thead}>
          <tr>
            {selectable && (
              <th className={cx(style.th, style.checkbox)}>
                <input type="checkbox" checked={isAllSelected} onChange={handleSelectAll} />
              </th>
            )}
            {columns.map((column) => (
              <th
                key={column.key}
                className={cx(
                  style.th,
                  column.className,
                  column.headerClass,
                  column.cellClass,
                  column.align === 'right' && style.th_right,
                  column.align === 'center' && style.th_center,
                )}
              >
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
          {sortedDatas.map((row) => {
            const key = rowKey(row)
            return (
              <tr key={key} className={style.tr}>
                {selectable && (
                  <td className={cx(style.td, style.checkbox)}>
                    <input type="checkbox" checked={selectedKeys?.has(key) ?? false} onChange={() => handleSelectRow(key)} />
                  </td>
                )}
                {columns.map((column) => (
                  <td key={column.key} className={cx(style.td, column.className, column.cellClass)}>
                    {column.cell(row)}
                  </td>
                ))}
              </tr>
            )
          })}
        </tbody>
      </table>
      {datas.length === 0 && <div className={style.empty}>データがありません</div>}
      {footer}
    </div>
  )
}
