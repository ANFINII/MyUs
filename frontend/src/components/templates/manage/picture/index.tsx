import { ChangeEvent, useMemo, useState } from 'react'
import { useRouter } from 'next/router'
import { Channel } from 'types/internal/channel'
import { Picture } from 'types/internal/media/output'
import { Option } from 'types/internal/other'
import { deleteManagePictures } from 'api/internal/manage/delete'
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
import SelectBox from 'components/parts/Input/SelectBox'
import Toggle from 'components/parts/Input/Toggle'
import Pagination from 'components/parts/Pagination'
import DeleteModal from 'components/widgets/Modal/Delete'
import style from '../Media.module.scss'

interface Props {
  datas: Picture[]
  channels: Channel[]
}

export default function ManagePictures(props: Props): React.JSX.Element {
  const { datas, channels } = props

  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))

  const router = useRouter()
  const { isLoading, handleLoading } = useIsLoading()
  const { toast, handleToast } = useToast()
  const { handleError } = useApiError({ handleToast })
  const [isDeleteModal, setIsDeleteModal] = useState<boolean>(false)
  const [selectedKeys, setSelectedKeys] = useState<Set<string>>(new Set())
  const [channelUlid, setChannelUlid] = useState<string>(channels[0]?.ulid ?? '')
  const channelDatas = useMemo(() => datas.filter((p) => p.channel.ulid === channelUlid), [datas, channelUlid])
  const { currentPage, totalPages, pageDatas, handlePage } = usePagination(channelDatas, 50)

  const handleDelete = () => setIsDeleteModal(!isDeleteModal)
  const handleEdit = (picture: Picture) => router.push(`/manage/picture/${picture.ulid}`)
  const handleChannel = (e: ChangeEvent<HTMLSelectElement>) => setChannelUlid(e.target.value)

  const handleDeleteSubmit = async () => {
    const ulids = Array.from(selectedKeys)
    if (ulids.length === 0) return

    handleLoading(true)
    const ret = await deleteManagePictures(ulids)
    handleLoading(false)
    if (ret.isErr()) {
      handleError(FetchError.Delete, ret.error.message)
      return
    }
    setSelectedKeys(new Set())
    handleDelete()
    router.replace(router.asPath)
  }

  const columns: Column<Picture>[] = [
    {
      key: 'thumbnail',
      header: '画像',
      className: style.thumbnail,
      cell: (p) => p.image && <ExImage src={p.image} width="96" height="54" />,
    },
    {
      key: 'title',
      header: 'タイトル',
      sortable: true,
      sortValue: (p) => p.title,
      className: style.title,
      cell: (p) => (
        <a className={style.title_link} onClick={() => handleEdit(p)}>
          {p.title}
        </a>
      ),
    },
    {
      key: 'content',
      header: '内容',
      className: style.content,
      cell: (p) => p.content,
    },
    {
      key: 'read',
      header: '閲覧',
      align: 'right',
      sortable: true,
      sortValue: (p) => p.read,
      className: style.normal,
      cellClass: style.number,
      cell: (p) => p.read,
    },
    {
      key: 'like',
      header: 'いいね',
      align: 'right',
      sortable: true,
      sortValue: (p) => p.like,
      className: style.normal,
      cellClass: style.number,
      cell: (p) => p.like,
    },
    {
      key: 'publish',
      header: '公開',
      align: 'center',
      sortable: true,
      sortValue: (p) => (p.publish ? 1 : 0),
      className: style.narrow,
      cellClass: style.publish,
      cell: (p) => (
        <div className={style.publish_inner}>
          <Toggle isActive={p.publish} disable />
        </div>
      ),
    },
    {
      key: 'created',
      header: '投稿日時',
      sortable: true,
      sortValue: (p) => new Date(p.created).getTime(),
      className: style.datetime,
      cell: (p) => formatDatetime(p.created),
    },
  ]

  return (
    <Main
      title="画像管理"
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
          datas={pageDatas}
          columns={columns}
          rowKey={(p) => p.ulid}
          selectable
          selectedKeys={selectedKeys}
          onSelection={setSelectedKeys}
          footer={<Pagination currentPage={currentPage} totalPages={totalPages} onChange={handlePage} />}
        />
      </div>
      <DeleteModal
        open={isDeleteModal}
        title="画像の削除"
        content={`${selectedKeys.size}件の画像を削除しますか？`}
        loading={isLoading}
        onClose={handleDelete}
        onAction={handleDeleteSubmit}
      />
    </Main>
  )
}
