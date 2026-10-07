import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQueryClient } from '@tanstack/react-query'
import { queryKeys } from 'lib/query/keys'
import { Channel } from 'types/internal/channel'
import { Chat, ChatList } from 'types/internal/media/output'
import { Option } from 'types/internal/other'
import { deleteManageChats } from 'api/internal/manage/delete'
import { FetchError } from 'utils/constants/enum'
import { useApiError } from 'components/hooks/useApiError'
import { useAppRouter } from 'components/hooks/useAppRouter'
import { useDatetime } from 'components/hooks/useDatetime'
import { useLoading } from 'components/hooks/useLoading'
import { usePagination } from 'components/hooks/usePagination'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import { Column } from 'components/parts/DataTable'
import Toggle from 'components/parts/Input/Toggle'
import style from '../Media.module.scss'
import ManageHeader from '../_container/Header'
import ManageTable from '../_container/Table'

interface Props {
  data: ChatList
  page: number
  channels: Channel[]
}

export default function ManageChats(props: Props): React.JSX.Element {
  const { data, page, channels } = props
  const { items, total } = data

  const router = useAppRouter()
  const { t } = useTranslation()
  const queryClient = useQueryClient()
  const { loading, handleLoading } = useLoading()
  const { toast, handleToast } = useToast()
  const { handleError } = useApiError({ handleToast })
  const { currentPage, totalPages, handlePage } = usePagination(total, page)
  const { formatDate, formatDatetime } = useDatetime()
  const [isModal, setIsModal] = useState<boolean>(false)
  const [selectedKeys, setSelectedKeys] = useState<Set<string>>(new Set())

  const handleModal = () => setIsModal(!isModal)
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
    handleModal()
    await queryClient.invalidateQueries({ queryKey: queryKeys.manageChats })
  }

  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))
  const channelUlid = router.query.channel?.toString() || channels[0]!.ulid

  const columns: Column<Chat>[] = [
    {
      key: 'title',
      header: t('manage.table.title'),
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
      header: t('manage.table.content'),
      className: style.content,
      cell: (c) => c.content,
    },
    {
      key: 'thread',
      header: t('manage.table.thread'),
      align: 'right',
      sortable: true,
      sortValue: (c) => c.thread,
      className: style.normal,
      cellClass: style.number,
      cell: (c) => c.thread,
    },
    {
      key: 'joined',
      header: t('manage.table.joined'),
      align: 'right',
      sortable: true,
      sortValue: (c) => c.joined,
      className: style.normal,
      cellClass: style.number,
      cell: (c) => c.joined,
    },
    {
      key: 'like',
      header: t('manage.table.like'),
      align: 'right',
      sortable: true,
      sortValue: (c) => c.like,
      className: style.normal,
      cellClass: style.number,
      cell: (c) => c.like,
    },
    {
      key: 'publish',
      header: t('manage.table.publish'),
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
      header: t('manage.table.deadline'),
      sortable: true,
      sortValue: (c) => new Date(c.period).getTime(),
      className: style.datetime,
      cell: (c) => formatDate(c.period),
    },
    {
      key: 'created',
      header: t('manage.table.created'),
      sortable: true,
      sortValue: (c) => new Date(c.created).getTime(),
      className: style.datetime,
      cell: (c) => formatDatetime(c.created),
    },
  ]

  return (
    <Main
      title="Chat"
      type="table"
      toast={toast}
      isFooter={false}
      button={<ManageHeader count={selectedKeys.size} ulid={channelUlid} options={channelOptions} onModal={handleModal} onChange={handleChannel} />}
    >
      <ManageTable
        table={{ datas: items, columns, rowKey: (c) => c.ulid }}
        selection={{ keys: selectedKeys, onChange: setSelectedKeys }}
        pagination={{ current: currentPage, total: totalPages, onChange: handlePage }}
        deletion={{ open: isModal, loading, onClose: handleModal, onAction: handleDeleteSubmit }}
      />
    </Main>
  )
}
