import { useState } from 'react'
import { useRouter } from 'next/router'
import { Advertise } from 'types/internal/advertise'
import { deleteManageAdvertises } from 'api/internal/manage/delete'
import { FetchError } from 'utils/constants/enum'
import { formatDatetime } from 'utils/functions/datetime'
import { useApiError } from 'components/hooks/useApiError'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { usePagination } from 'components/hooks/usePagination'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import DataTable, { Column } from 'components/parts/DataTable'
import ExImage from 'components/parts/ExImage'
import Toggle from 'components/parts/Input/Toggle'
import Pagination from 'components/parts/Pagination'
import DeleteModal from 'components/widgets/Modal/Delete'
import style from '../Media.module.scss'

interface Props {
  datas: Advertise[]
  total: number
  page: number
}

const ADVERTISE_LIMIT = 5

export default function ManageAdvertises(props: Props): React.JSX.Element {
  const { datas, total, page } = props

  const router = useRouter()
  const { isLoading, handleLoading } = useIsLoading()
  const { toast, handleToast } = useToast()
  const { handleError } = useApiError({ handleToast })
  const { currentPage, totalPages, handlePage } = usePagination(total, page)
  const [isDeleteModal, setIsDeleteModal] = useState<boolean>(false)
  const [selectedKeys, setSelectedKeys] = useState<Set<string>>(new Set())

  const handleDelete = () => setIsDeleteModal(!isDeleteModal)
  const handleEdit = (advertise: Advertise) => router.push(`/manage/advertise/${advertise.ulid}`)
  const handleCreate = () => router.push('/manage/advertise/create')

  const handleDeleteSubmit = async () => {
    const ulids = Array.from(selectedKeys)
    if (ulids.length === 0) return

    handleLoading(true)
    const ret = await deleteManageAdvertises(ulids)
    handleLoading(false)
    if (ret.isErr()) {
      handleError(FetchError.Delete, ret.error.message)
      return
    }
    setSelectedKeys(new Set())
    handleDelete()
    router.replace(router.asPath)
  }

  const isLimitReached = total >= ADVERTISE_LIMIT

  const columns: Column<Advertise>[] = [
    {
      key: 'thumbnail',
      header: '画像',
      className: style.thumbnail,
      cell: (a) => a.image && <ExImage src={a.image} width="96" height="54" />,
    },
    {
      key: 'title',
      header: 'タイトル',
      sortable: true,
      sortValue: (a) => a.title,
      className: style.title,
      cell: (a) => (
        <a className={style.title_link} onClick={() => handleEdit(a)}>
          {a.title}
        </a>
      ),
    },
    {
      key: 'url',
      header: 'URL',
      className: style.content,
      cell: (a) => a.url,
    },
    {
      key: 'read',
      header: '閲覧',
      align: 'right',
      sortable: true,
      sortValue: (a) => a.read,
      className: style.normal,
      cellClass: style.number,
      cell: (a) => a.read,
    },
    {
      key: 'period',
      header: '表示期限',
      align: 'center',
      className: style.normal,
      cell: (a) => a.period ?? '-',
    },
    {
      key: 'publish',
      header: '公開',
      align: 'center',
      sortable: true,
      sortValue: (a) => (a.publish ? 1 : 0),
      className: style.narrow,
      cellClass: style.publish,
      cell: (a) => (
        <div className={style.publish_inner}>
          <Toggle isActive={a.publish} disable />
        </div>
      ),
    },
    {
      key: 'created',
      header: '作成日時',
      sortable: true,
      sortValue: (a) => new Date(a.created).getTime(),
      className: style.datetime,
      cell: (a) => formatDatetime(a.created),
    },
  ]

  return (
    <Main
      title="広告管理"
      type="table"
      toast={toast}
      isFooter={false}
      button={
        <div className={style.header_actions}>
          {selectedKeys.size > 0 && (
            <>
              <span className={style.selected_count}>{selectedKeys.size}件選択</span>
              <Button color="red" size="s" name="一括削除" onClick={handleDelete} />
            </>
          )}
          <Button color="green" size="s" name={`作成 (${total}/${ADVERTISE_LIMIT})`} disabled={isLimitReached} onClick={handleCreate} />
        </div>
      }
    >
      <div className={style.manage}>
        <DataTable
          datas={datas}
          columns={columns}
          rowKey={(a) => a.ulid}
          selectable
          selectedKeys={selectedKeys}
          onSelection={setSelectedKeys}
          footer={<Pagination currentPage={currentPage} totalPages={totalPages} onChange={handlePage} />}
        />
      </div>
      <DeleteModal
        open={isDeleteModal}
        title="広告の削除"
        content={`${selectedKeys.size}件の広告を削除しますか？`}
        loading={isLoading}
        onClose={handleDelete}
        onAction={handleDeleteSubmit}
      />
    </Main>
  )
}
