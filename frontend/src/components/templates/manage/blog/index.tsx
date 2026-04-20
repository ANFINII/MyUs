import { ChangeEvent, useMemo, useState } from 'react'
import { useRouter } from 'next/router'
import { Channel } from 'types/internal/channel'
import { Blog } from 'types/internal/media/output'
import { Option } from 'types/internal/other'
import { deleteManageBlogs } from 'api/internal/manage/delete'
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
  datas: Blog[]
  channels: Channel[]
}

export default function ManageBlogs(props: Props): React.JSX.Element {
  const { datas, channels } = props

  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))

  const router = useRouter()
  const { isLoading, handleLoading } = useIsLoading()
  const { toast, handleToast } = useToast()
  const { handleError } = useApiError({ handleToast })
  const [isDeleteModal, setIsDeleteModal] = useState<boolean>(false)
  const [selectedKeys, setSelectedKeys] = useState<Set<string>>(new Set())
  const [channelUlid, setChannelUlid] = useState<string>(channels[0]?.ulid ?? '')
  const channelDatas = useMemo(() => datas.filter((b) => b.channel.ulid === channelUlid), [datas, channelUlid])
  const { currentPage, totalPages, pageDatas, handlePage } = usePagination(channelDatas, 50)

  const handleDelete = () => setIsDeleteModal(!isDeleteModal)
  const handleEdit = (blog: Blog) => router.push(`/manage/blog/${blog.ulid}`)
  const handleChannel = (e: ChangeEvent<HTMLSelectElement>) => setChannelUlid(e.target.value)

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
    handleDelete()
    router.replace(router.asPath)
  }

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
      title="ブログ管理"
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
          rowKey={(b) => b.ulid}
          selectable
          selectedKeys={selectedKeys}
          onSelection={setSelectedKeys}
          footer={<Pagination currentPage={currentPage} totalPages={totalPages} onChange={handlePage} />}
        />
      </div>
      <DeleteModal
        open={isDeleteModal}
        title="ブログの削除"
        content={`${selectedKeys.size}件のブログを削除しますか？`}
        loading={isLoading}
        onClose={handleDelete}
        onAction={handleDeleteSubmit}
      />
    </Main>
  )
}
