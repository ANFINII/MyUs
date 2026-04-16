import { ChangeEvent, useMemo, useState } from 'react'
import { useRouter } from 'next/router'
import { Channel } from 'types/internal/channel'
import { Video } from 'types/internal/media'
import { Option } from 'types/internal/other'
import { deleteManageVideos } from 'api/internal/manage/video'
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
import style from '../Manage.module.scss'

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
  const [isDeleteModal, setIsDeleteModal] = useState<boolean>(false)
  const [selectedKeys, setSelectedKeys] = useState<Set<string>>(new Set())
  const [channelUlid, setChannelUlid] = useState<string>(channels[0]?.ulid ?? '')

  const handleDelete = () => setIsDeleteModal(!isDeleteModal)
  const handleEdit = (video: Video) => router.push(`/manage/video/${video.ulid}`)
  const handleChannel = (e: ChangeEvent<HTMLSelectElement>) => setChannelUlid(e.target.value)

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

  const channelDatas = useMemo(() => {
    return datas.filter((v) => v.channel.ulid === channelUlid)
  }, [datas, channelUlid])

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
      key: 'created',
      header: '投稿日時',
      sortable: true,
      sortValue: (v) => new Date(v.created).getTime(),
      className: style.datetime,
      cell: (v) => formatDatetime(v.created),
    },
    {
      key: 'read',
      header: '再生',
      align: 'right',
      sortable: true,
      sortValue: (v) => v.read,
      className: style.narrow,
      cellClass: style.number,
      cell: (v) => v.read,
    },
    {
      key: 'like',
      header: 'いいね',
      align: 'right',
      sortable: true,
      sortValue: (v) => v.like,
      className: style.narrow,
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
  ]

  return (
    <Main
      title="動画管理"
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
        <DataTable datas={channelDatas} columns={columns} rowKey={(v) => v.ulid} selectable selectedKeys={selectedKeys} onSelection={setSelectedKeys} />
      </div>
      <DeleteModal
        open={isDeleteModal}
        title="動画の削除"
        content={`${selectedKeys.size}件の動画を削除しますか？`}
        loading={isLoading}
        onClose={handleDelete}
        onAction={handleDeleteSubmit}
      />
    </Main>
  )
}
