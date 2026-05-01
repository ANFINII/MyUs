import { ChangeEvent, useState } from 'react'
import { useRouter } from 'next/router'
import { Channel } from 'types/internal/channel'
import { Music } from 'types/internal/media/output'
import { Option } from 'types/internal/other'
import { deleteManageMusics } from 'api/internal/manage/delete'
import { FetchError } from 'utils/constants/enum'
import { formatDatetime } from 'utils/functions/datetime'
import { useApiError } from 'components/hooks/useApiError'
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
  datas: Music[]
  total: number
  page: number
  channels: Channel[]
}

export default function ManageMusics(props: Props): React.JSX.Element {
  const { datas, total, page, channels } = props

  const router = useRouter()
  const { loading, handleLoading } = useLoading()
  const { toast, handleToast } = useToast()
  const { handleError } = useApiError({ handleToast })
  const { currentPage, totalPages, handlePage } = usePagination(total, page)
  const [isDeleteModal, setIsDeleteModal] = useState<boolean>(false)
  const [selectedKeys, setSelectedKeys] = useState<Set<string>>(new Set())

  const handleDelete = () => setIsDeleteModal(!isDeleteModal)
  const handleEdit = (music: Music) => router.push(`/manage/music/${music.ulid}`)

  const handleChannel = (e: ChangeEvent<HTMLSelectElement>) => {
    router.push({ pathname: router.pathname, query: { ...router.query, channel: e.target.value, page: 1 } })
  }

  const handleDeleteSubmit = async () => {
    const ulids = Array.from(selectedKeys)
    if (ulids.length === 0) return

    handleLoading(true)
    const ret = await deleteManageMusics(ulids)
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

  const columns: Column<Music>[] = [
    {
      key: 'title',
      header: 'タイトル',
      sortable: true,
      sortValue: (m) => m.title,
      className: style.title,
      cell: (m) => (
        <a className={style.title_link} onClick={() => handleEdit(m)}>
          {m.title}
        </a>
      ),
    },
    {
      key: 'content',
      header: '内容',
      className: style.content,
      cell: (m) => m.content,
    },
    {
      key: 'read',
      header: '再生',
      align: 'right',
      sortable: true,
      sortValue: (m) => m.read,
      className: style.normal,
      cellClass: style.number,
      cell: (m) => m.read,
    },
    {
      key: 'like',
      header: 'いいね',
      align: 'right',
      sortable: true,
      sortValue: (m) => m.like,
      className: style.normal,
      cellClass: style.number,
      cell: (m) => m.like,
    },
    {
      key: 'download',
      header: 'DL',
      align: 'center',
      sortable: true,
      sortValue: (m) => (m.download ? 1 : 0),
      className: style.narrow,
      cellClass: style.publish,
      cell: (m) => (
        <div className={style.publish_inner}>
          <Toggle isActive={m.download} disable />
        </div>
      ),
    },
    {
      key: 'publish',
      header: '公開',
      align: 'center',
      sortable: true,
      sortValue: (m) => (m.publish ? 1 : 0),
      className: style.narrow,
      cellClass: style.publish,
      cell: (m) => (
        <div className={style.publish_inner}>
          <Toggle isActive={m.publish} disable />
        </div>
      ),
    },
    {
      key: 'created',
      header: '投稿日時',
      sortable: true,
      sortValue: (m) => new Date(m.created).getTime(),
      className: style.datetime,
      cell: (m) => formatDatetime(m.created),
    },
  ]

  return (
    <Main
      title="Music"
      type="table"
      toast={toast}
      isFooter={false}
      button={<ManageHeader count={selectedKeys.size} ulid={channelUlid} options={channelOptions} onDelete={handleDelete} onChange={handleChannel} />}
    >
      <ManageTable
        table={{ datas, columns, rowKey: (m) => m.ulid }}
        selection={{ keys: selectedKeys, onChange: setSelectedKeys }}
        pagination={{ current: currentPage, total: totalPages, onChange: handlePage }}
        deletion={{ open: isDeleteModal, loading, onClose: handleDelete, onAction: handleDeleteSubmit }}
      />
    </Main>
  )
}
