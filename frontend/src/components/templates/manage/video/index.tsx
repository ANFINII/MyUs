import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQueryClient } from '@tanstack/react-query'
import { queryKeys } from 'lib/query/keys'
import { Channel } from 'types/internal/channel'
import { Video, VideoList } from 'types/internal/media/output'
import { Option } from 'types/internal/other'
import { deleteManageVideos } from 'api/internal/manage/delete'
import { FetchError } from 'utils/constants/enum'
import { useApiError } from 'components/hooks/useApiError'
import { useDatetime } from 'components/hooks/useDatetime'
import { useLoading } from 'components/hooks/useLoading'
import { usePagination } from 'components/hooks/usePagination'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import { Column } from 'components/parts/DataTable'
import ExImage from 'components/parts/ExImage'
import Toggle from 'components/parts/Input/Toggle'
import style from '../Media.module.scss'
import ManageHeader from '../_container/Header'
import ManageTable from '../_container/Table'

interface Props {
  data: VideoList
  page: number
  channels: Channel[]
}

export default function ManageVideos(props: Props): React.JSX.Element {
  const { data, page, channels } = props
  const { items, total } = data

  const router = useRouter()
  const { t } = useTranslation()
  const queryClient = useQueryClient()
  const { loading, handleLoading } = useLoading()
  const { toast, handleToast } = useToast()
  const { handleError } = useApiError({ handleToast })
  const { currentPage, totalPages, handlePage } = usePagination(total, page)
  const { formatDatetime } = useDatetime()
  const [isModal, setIsModal] = useState<boolean>(false)
  const [selectedKeys, setSelectedKeys] = useState<Set<string>>(new Set())

  const handleModal = () => setIsModal(!isModal)
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
    handleModal()
    await queryClient.invalidateQueries({ queryKey: queryKeys.manageVideos })
  }

  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))
  const channelUlid = router.query.channel?.toString() || channels[0]!.ulid

  const columns: Column<Video>[] = [
    {
      key: 'thumbnail',
      header: t('manage.table.thumbnail'),
      className: style.thumbnail,
      cell: (v) => v.image && <ExImage src={v.image} width="96" height="54" />,
    },
    {
      key: 'title',
      header: t('manage.table.title'),
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
      header: t('manage.table.content'),
      className: style.content,
      cell: (v) => v.content,
    },
    {
      key: 'read',
      header: t('manage.table.play'),
      align: 'right',
      sortable: true,
      sortValue: (v) => v.read,
      className: style.normal,
      cellClass: style.number,
      cell: (v) => v.read,
    },
    {
      key: 'like',
      header: t('manage.table.like'),
      align: 'right',
      sortable: true,
      sortValue: (v) => v.like,
      className: style.normal,
      cellClass: style.number,
      cell: (v) => v.like,
    },
    {
      key: 'publish',
      header: t('manage.table.publish'),
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
      header: t('manage.table.created'),
      sortable: true,
      sortValue: (v) => new Date(v.created).getTime(),
      className: style.datetime,
      cell: (v) => formatDatetime(v.created),
    },
  ]

  return (
    <Main
      title="Video"
      type="table"
      toast={toast}
      isFooter={false}
      button={<ManageHeader count={selectedKeys.size} ulid={channelUlid} options={channelOptions} onModal={handleModal} onChange={handleChannel} />}
    >
      <ManageTable
        table={{ datas: items, columns, rowKey: (v) => v.ulid }}
        selection={{ keys: selectedKeys, onChange: setSelectedKeys }}
        pagination={{ current: currentPage, total: totalPages, onChange: handlePage }}
        deletion={{ open: isModal, loading, onClose: handleModal, onAction: handleDeleteSubmit }}
      />
    </Main>
  )
}
