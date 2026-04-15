import { ChangeEvent, useMemo, useState } from 'react'
import { useRouter } from 'next/router'
import { Channel } from 'types/internal/channel'
import { Video } from 'types/internal/media'
import { Option } from 'types/internal/other'
import { deleteManageVideo } from 'api/internal/manage/video'
import { FetchError } from 'utils/constants/enum'
import { formatDatetime } from 'utils/functions/datetime'
import { useApiError } from 'components/hooks/useApiError'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import DataTable, { Column } from 'components/parts/DataTable'
import ExImage from 'components/parts/ExImage'
import SelectBox from 'components/parts/Input/SelectBox'
import Toggle from 'components/parts/Input/Toggle'
import DeleteModal from 'components/widgets/Modal/Delete'
import style from './Video.module.scss'

interface Props {
  datas: Video[]
  channels: Channel[]
}

export default function ManageVideos(props: Props): React.JSX.Element {
  const { datas, channels } = props

  const router = useRouter()
  const { isLoading, handleLoading } = useIsLoading()
  const { toast, handleToast } = useToast()
  const { handleError } = useApiError({ handleToast })
  const [deleteTarget, setDeleteTarget] = useState<Video | null>(null)
  const [channelUlid, setChannelUlid] = useState<string>(channels[0]?.ulid ?? '')

  const handleChannel = (e: ChangeEvent<HTMLSelectElement>) => setChannelUlid(e.target.value)
  const handleEdit = (video: Video) => router.push(`/manage/media/video/edit/${video.ulid}`)
  const handleDeleteOpen = (video: Video) => setDeleteTarget(video)
  const handleDeleteClose = () => setDeleteTarget(null)

  const handleDeleteSubmit = async () => {
    if (!deleteTarget) return
    handleLoading(true)
    const ret = await deleteManageVideo(deleteTarget.ulid)
    handleLoading(false)
    if (ret.isErr()) {
      handleError(FetchError.Delete, ret.error.message)
      return
    }
    handleDeleteClose()
    router.replace(router.asPath)
  }

  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))

  const channelDatas = useMemo(() => {
    return datas.filter((v) => v.channel.ulid === channelUlid)
  }, [datas, channelUlid])

  const columns: Column<Video>[] = [
    {
      key: 'thumbnail',
      header: 'サムネイル',
      className: style.thumbnail,
      render: (v) => v.image && <ExImage src={v.image} width="96" height="54" />,
    },
    {
      key: 'title',
      header: 'タイトル',
      sortable: true,
      sortValue: (v) => v.title,
      className: style.title,
      render: (v) => v.title,
    },
    {
      key: 'content',
      header: '内容',
      sortable: true,
      sortValue: (v) => v.content,
      className: style.content,
      render: (v) => v.content,
    },
    {
      key: 'created',
      header: '投稿日時',
      sortable: true,
      sortValue: (v) => new Date(v.created).getTime(),
      className: style.datetime,
      render: (v) => formatDatetime(v.created),
    },
    {
      key: 'read',
      header: '再生',
      sortable: true,
      sortValue: (v) => v.read,
      className: style.narrow,
      cellClass: style.number,
      render: (v) => v.read,
    },
    {
      key: 'like',
      header: 'いいね',
      sortable: true,
      sortValue: (v) => v.like,
      className: style.narrow,
      cellClass: style.number,
      render: (v) => v.like,
    },
    {
      key: 'publish',
      header: '公開',
      sortable: true,
      sortValue: (v) => (v.publish ? 1 : 0),
      className: style.narrow,
      headerClass: style.center,
      cellClass: style.publish,
      render: (v) => (
        <div className={style.publish_inner}>
          <Toggle isActive={v.publish} disable />
        </div>
      ),
    },
    {
      key: 'actions',
      header: '操作',
      className: style.actions,
      render: (v) => (
        <div className={style.actions_inner}>
          <Button color="blue" size="s" name="編集" onClick={() => handleEdit(v)} />
          <Button color="red" size="s" name="削除" onClick={() => handleDeleteOpen(v)} />
        </div>
      ),
    },
  ]

  return (
    <Main title="動画管理" type="table" toast={toast} button={<SelectBox value={channelUlid} options={channelOptions} className={style.filter} onChange={handleChannel} />}>
      <div className={style.manage}>
        <DataTable datas={channelDatas} columns={columns} rowKey={(v) => v.ulid} />
      </div>
      <DeleteModal
        open={deleteTarget !== null}
        title="動画の削除"
        content={`「${deleteTarget?.title ?? ''}」を削除しますか？`}
        loading={isLoading}
        onClose={handleDeleteClose}
        onAction={handleDeleteSubmit}
      />
    </Main>
  )
}
