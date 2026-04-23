import { ChangeEvent, useState } from 'react'
import { useRouter } from 'next/router'
import { Channel } from 'types/internal/channel'
import { Chat } from 'types/internal/media/output'
import { Option } from 'types/internal/other'
import { deleteManageChats } from 'api/internal/manage/delete'
import { FetchError } from 'utils/constants/enum'
import { formatDate, formatDatetime } from 'utils/functions/datetime'
import { useApiError } from 'components/hooks/useApiError'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { usePagination } from 'components/hooks/usePagination'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import DataTable, { Column } from 'components/parts/DataTable'
import SelectBox from 'components/parts/Input/SelectBox'
import Toggle from 'components/parts/Input/Toggle'
import Pagination from 'components/parts/Pagination'
import DeleteModal from 'components/widgets/Modal/Delete'
import style from '../Media.module.scss'

interface Props {
  datas: Chat[]
  total: number
  page: number
  channels: Channel[]
}

export default function ManageChats(props: Props): React.JSX.Element {
  const { datas, total, page, channels } = props

  const router = useRouter()
  const { isLoading, handleLoading } = useIsLoading()
  const { toast, handleToast } = useToast()
  const { handleError } = useApiError({ handleToast })
  const { currentPage, totalPages, handlePage } = usePagination(total, page)
  const [isDeleteModal, setIsDeleteModal] = useState<boolean>(false)
  const [selectedKeys, setSelectedKeys] = useState<Set<string>>(new Set())

  const handleDelete = () => setIsDeleteModal(!isDeleteModal)
  const handleEdit = (chat: Chat) => router.push(`/manage/chat/${chat.ulid}`)

  const handleChannel = (e: ChangeEvent<HTMLSelectElement>) => {
    router.push({ pathname: router.pathname, query: { ...router.query, channel: e.target.value, page: 1 } })
  }

  const handleDeleteSubmit = async () => {
    const ulids = Array.from(selectedKeys)
    if (ulids.length === 0) return

    handleLoading(true)
    const ret = await deleteManageChats(ulids)
    handleLoading(false)
    if (ret.isErr()) {
      handleError(FetchError.Delete, ret.error.message)
      return
    }
    setSelectedKeys(new Set())
    handleDelete()
    router.replace(router.asPath)
  }

  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))
  const channelUlid = router.query.channel?.toString() || channels[0]!.ulid

  const columns: Column<Chat>[] = [
    {
      key: 'title',
      header: 'タイトル',
      sortable: true,
      sortValue: (c) => c.title,
      className: style.title,
      cell: (c) => (
        <a className={style.title_link} onClick={() => handleEdit(c)}>
          {c.title}
        </a>
      ),
    },
    {
      key: 'content',
      header: '内容',
      className: style.content,
      cell: (c) => c.content,
    },
    {
      key: 'thread',
      header: 'スレッド',
      align: 'right',
      sortable: true,
      sortValue: (c) => c.thread,
      className: style.normal,
      cellClass: style.number,
      cell: (c) => c.thread,
    },
    {
      key: 'joined',
      header: '参加',
      align: 'right',
      sortable: true,
      sortValue: (c) => c.joined,
      className: style.normal,
      cellClass: style.number,
      cell: (c) => c.joined,
    },
    {
      key: 'like',
      header: 'いいね',
      align: 'right',
      sortable: true,
      sortValue: (c) => c.like,
      className: style.normal,
      cellClass: style.number,
      cell: (c) => c.like,
    },
    {
      key: 'publish',
      header: '公開',
      align: 'center',
      sortable: true,
      sortValue: (c) => (c.publish ? 1 : 0),
      className: style.narrow,
      cellClass: style.publish,
      cell: (c) => (
        <div className={style.publish_inner}>
          <Toggle isActive={c.publish} disable />
        </div>
      ),
    },
    {
      key: 'period',
      header: '期限',
      sortable: true,
      sortValue: (c) => new Date(c.period).getTime(),
      className: style.datetime,
      cell: (c) => formatDate(c.period),
    },
    {
      key: 'created',
      header: '投稿日時',
      sortable: true,
      sortValue: (c) => new Date(c.created).getTime(),
      className: style.datetime,
      cell: (c) => formatDatetime(c.created),
    },
  ]

  return (
    <Main
      title="チャット管理"
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
          <SelectBox value={channelUlid} options={channelOptions} className={style.filter} onChange={handleChannel} />
        </div>
      }
    >
      <div className={style.manage}>
        <DataTable
          datas={datas}
          columns={columns}
          rowKey={(c) => c.ulid}
          selectable
          selectedKeys={selectedKeys}
          onSelection={setSelectedKeys}
          footer={<Pagination currentPage={currentPage} totalPages={totalPages} onChange={handlePage} />}
        />
      </div>
      <DeleteModal
        open={isDeleteModal}
        title="チャットの削除"
        content={`${selectedKeys.size}件のチャットを削除しますか？`}
        loading={isLoading}
        onClose={handleDelete}
        onAction={handleDeleteSubmit}
      />
    </Main>
  )
}
