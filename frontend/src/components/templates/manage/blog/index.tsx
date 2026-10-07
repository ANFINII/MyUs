import { ChangeEvent, useState } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { queryKeys } from 'lib/query/keys'
import { Channel } from 'types/internal/channel'
import { Blog, BlogList } from 'types/internal/media/output'
import { Option } from 'types/internal/other'
import { deleteManageBlogs } from 'api/internal/manage/delete'
import { FetchError } from 'utils/constants/enum'
import { useApiError } from 'components/hooks/useApiError'
import { useAppRouter } from 'components/hooks/useAppRouter'
import { useDatetime } from 'components/hooks/useDatetime'
import { useLoading } from 'components/hooks/useLoading'
import { usePagination } from 'components/hooks/usePagination'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import { Column } from 'components/parts/DataTable'
import ExImage from 'components/parts/ExImage'
import Toggle from 'components/parts/Input/Toggle'
import style from '../Media.module.scss'
import ManageHeader from '../_container/Header'
import ManageTable from '../_container/Table'

interface Props {
  data: BlogList
  page: number
  channels: Channel[]
}

export default function ManageBlogs(props: Props): React.JSX.Element {
  const { data, page, channels } = props
  const { items, total } = data

  const router = useAppRouter()
  const queryClient = useQueryClient()
  const { loading, handleLoading } = useLoading()
  const { toast, handleToast } = useToast()
  const { handleError } = useApiError({ handleToast })
  const { currentPage, totalPages, handlePage } = usePagination(total, page)
  const { formatDatetime } = useDatetime()
  const [isModal, setIsModal] = useState<boolean>(false)
  const [selectedKeys, setSelectedKeys] = useState<Set<string>>(new Set())

  const handleModal = () => setIsModal(!isModal)
  const handleEdit = (blog: Blog) => router.push(`/manage/blog/${blog.ulid}`)

  const handleChannel = (e: ChangeEvent<HTMLSelectElement>) => {
    router.push({ pathname: router.pathname, query: { ...router.query, channel: e.target.value, page: 1 } })
  }

  const handleDeleteSubmit = async () => {
    const ulids = Array.from(selectedKeys)
    if (ulids.length === 0) return

    handleLoading(true)
    const ret = await deleteManageBlogs(ulids)
    handleLoading(false)
    if (ret.isErr()) {
      handleError(FetchError.Delete, ret.error.message)
      return
    }
    setSelectedKeys(new Set())
    handleModal()
    await queryClient.invalidateQueries({ queryKey: queryKeys.manageBlogs })
  }

  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))
  const channelUlid = router.query.channel?.toString() || channels[0]!.ulid

  const columns: Column<Blog>[] = [
    {
      key: 'thumbnail',
      header: 'サムネイル',
      className: style.thumbnail,
      cell: (b) => b.image && <ExImage src={b.image} width="96" height="54" />,
    },
    {
      key: 'title',
      header: 'タイトル',
      sortable: true,
      sortValue: (b) => b.title,
      className: style.title,
      cell: (b) => (
        <a className={style.title_link} onClick={() => handleEdit(b)}>
          {b.title}
        </a>
      ),
    },
    {
      key: 'content',
      header: '内容',
      className: style.content,
      cell: (b) => b.content,
    },
    {
      key: 'read',
      header: '閲覧',
      align: 'right',
      sortable: true,
      sortValue: (b) => b.read,
      className: style.normal,
      cellClass: style.number,
      cell: (b) => b.read,
    },
    {
      key: 'like',
      header: 'いいね',
      align: 'right',
      sortable: true,
      sortValue: (b) => b.like,
      className: style.normal,
      cellClass: style.number,
      cell: (b) => b.like,
    },
    {
      key: 'publish',
      header: '公開',
      align: 'center',
      sortable: true,
      sortValue: (b) => (b.publish ? 1 : 0),
      className: style.narrow,
      cellClass: style.publish,
      cell: (b) => (
        <div className={style.publish_inner}>
          <Toggle isActive={b.publish} disable />
        </div>
      ),
    },
    {
      key: 'created',
      header: '投稿日時',
      sortable: true,
      sortValue: (b) => new Date(b.created).getTime(),
      className: style.datetime,
      cell: (b) => formatDatetime(b.created),
    },
  ]

  return (
    <Main
      title="Blog"
      type="table"
      toast={toast}
      isFooter={false}
      button={<ManageHeader count={selectedKeys.size} ulid={channelUlid} options={channelOptions} onModal={handleModal} onChange={handleChannel} />}
    >
      <ManageTable
        table={{ datas: items, columns, rowKey: (b) => b.ulid }}
        selection={{ keys: selectedKeys, onChange: setSelectedKeys }}
        pagination={{ current: currentPage, total: totalPages, onChange: handlePage }}
        deletion={{ open: isModal, loading, onClose: handleModal, onAction: handleDeleteSubmit }}
      />
    </Main>
  )
}
