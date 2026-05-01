import { ChangeEvent, useState } from 'react'
import { useRouter } from 'next/router'
import { Channel } from 'types/internal/channel'
import { Video } from 'types/internal/media/output'
import { Option } from 'types/internal/other'
import { deleteManageVideos } from 'api/internal/manage/delete'
import { FetchError } from 'utils/constants/enum'
import { formatDatetime } from 'utils/functions/datetime'
import { useApiError } from 'components/hooks/useApiError'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { usePagination } from 'components/hooks/usePagination'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import { Column } from 'components/parts/DataTable'
import ExImage from 'components/parts/ExImage'
import Toggle from 'components/parts/Input/Toggle'
import style from '../Media.module.scss'
import ManageHeader from '../_container/Header'
import ManageList from '../_container/List'

interface Props {
  datas: Video[]
  total: number
  page: number
  channels: Channel[]
}

export default function ManageVideos(props: Props): React.JSX.Element {
  const { datas, total, page, channels } = props

  const router = useRouter()
  const { isLoading, handleLoading } = useIsLoading()
  const { toast, handleToast } = useToast()
  const { handleError } = useApiError({ handleToast })
  const { currentPage, totalPages, handlePage } = usePagination(total, page)
  const [isDeleteModal, setIsDeleteModal] = useState<boolean>(false)
  const [selectedKeys, setSelectedKeys] = useState<Set<string>>(new Set())

  const handleDelete = () => setIsDeleteModal(!isDeleteModal)
  const handleEdit = (video: Video) => router.push(`/manage/video/${video.ulid}`)

  const handleChannel = (e: ChangeEvent<HTMLSelectElement>) => {
    router.push({ pathname: router.pathname, query: { ...router.query, channel: e.target.value, page: 1 } })
  }

  const handleDeleteSubmit = async () => {
    const ulids = Array.from(selectedKeys)
    if (ulids.length === 0) return

    handleLoading(true)
    const ret = await deleteManageVideos(ulids)
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

  const columns: Column<Video>[] = [
    {
      key: 'thumbnail',
      header: 'サムネイル',
      className: style.thumbnail,
      cell: (v) => v.image && <ExImage src={v.image} width="96" height="54" />,
    },
    {
      key: 'title',
      header: 'タイトル',
      sortable: true,
      sortValue: (v) => v.title,
      className: style.title,
      cell: (v) => (
        <a className={style.title_link} onClick={() => handleEdit(v)}>
          {v.title}
        </a>
      ),
    },
    {
      key: 'content',
      header: '内容',
      className: style.content,
      cell: (v) => v.content,
    },
    {
      key: 'read',
      header: '再生',
      align: 'right',
      sortable: true,
      sortValue: (v) => v.read,
      className: style.normal,
      cellClass: style.number,
      cell: (v) => v.read,
    },
    {
      key: 'like',
      header: 'いいね',
      align: 'right',
      sortable: true,
      sortValue: (v) => v.like,
      className: style.normal,
      cellClass: style.number,
      cell: (v) => v.like,
    },
    {
      key: 'publish',
      header: '公開',
      align: 'center',
      sortable: true,
      sortValue: (v) => (v.publish ? 1 : 0),
      className: style.narrow,
      cellClass: style.publish,
      cell: (v) => (
        <div className={style.publish_inner}>
          <Toggle isActive={v.publish} disable />
        </div>
      ),
    },
    {
      key: 'created',
      header: '投稿日時',
      sortable: true,
      sortValue: (v) => new Date(v.created).getTime(),
      className: style.datetime,
      cell: (v) => formatDatetime(v.created),
    },
  ]

  return (
    <Main
      title="動画管理"
      type="table"
      toast={toast}
      isFooter={false}
      button={<ManageHeader count={selectedKeys.size} ulid={channelUlid} options={channelOptions} onDelete={handleDelete} onChange={handleChannel} />}
    >
      <ManageList<Video>
        table={{ datas, columns, rowKey: (v) => v.ulid }}
        selection={{ keys: selectedKeys, onChange: setSelectedKeys }}
        pagination={{ current: currentPage, total: totalPages, onChange: handlePage }}
        deletion={{ label: '動画', open: isDeleteModal, loading: isLoading, onClose: handleDelete, onAction: handleDeleteSubmit }}
      />
    </Main>
  )
}
