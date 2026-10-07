import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQueryClient } from '@tanstack/react-query'
import { queryKeys } from 'lib/query/keys'
import { Advertise, AdvertiseList } from 'types/internal/advertise'
import { deleteManageAdvertises } from 'api/internal/manage/delete'
import { FetchError } from 'utils/constants/enum'
import { useApiError } from 'components/hooks/useApiError'
import { useDatetime } from 'components/hooks/useDatetime'
import { useLoading } from 'components/hooks/useLoading'
import { usePagination } from 'components/hooks/usePagination'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import { Column } from 'components/parts/DataTable'
import ExImage from 'components/parts/ExImage'
import Toggle from 'components/parts/Input/Toggle'
import style from '../Media.module.scss'
import ManageTable from '../_container/Table'

interface Props {
  data: AdvertiseList
  page: number
}

const ADVERTISE_LIMIT = 5

export default function ManageAdvertises(props: Props): React.JSX.Element {
  const { data, page } = props
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
  const handleEdit = (advertise: Advertise) => router.push(`/manage/advertise/${advertise.ulid}`)
  const handleCreate = () => router.push('/manage/advertise/create')

  const handleDeleteSubmit = async () => {
    const ulids = Array.from(selectedKeys)
    if (ulids.length === 0) return

    handleLoading(true)
    const ret = await deleteManageAdvertises(ulids)
    handleLoading(false)
    if (ret.isErr()) {
      handleError(FetchError.Delete, ret.error.message)
      return
    }
    setSelectedKeys(new Set())
    handleModal()
    await queryClient.invalidateQueries({ queryKey: queryKeys.manageAdvertises })
  }

  const isLimitReached = total >= ADVERTISE_LIMIT

  const columns: Column<Advertise>[] = [
    {
      key: 'thumbnail',
      header: t('manage.table.image'),
      className: style.thumbnail,
      cell: (a) => a.image && <ExImage src={a.image} width="96" height="54" />,
    },
    {
      key: 'title',
      header: t('manage.table.title'),
      sortable: true,
      sortValue: (a) => a.title,
      className: style.title,
      cell: (a) => (
        <a className={style.title_link} onClick={() => handleEdit(a)}>
          {a.title}
        </a>
      ),
    },
    {
      key: 'url',
      header: 'URL',
      className: style.content,
      cell: (a) => a.url,
    },
    {
      key: 'read',
      header: t('manage.table.view'),
      align: 'right',
      sortable: true,
      sortValue: (a) => a.read,
      className: style.normal,
      cellClass: style.number,
      cell: (a) => a.read,
    },
    {
      key: 'period',
      header: t('manage.table.displayPeriod'),
      align: 'center',
      className: style.normal,
      cell: (a) => a.period ?? '-',
    },
    {
      key: 'publish',
      header: t('manage.table.publish'),
      align: 'center',
      sortable: true,
      sortValue: (a) => (a.publish ? 1 : 0),
      className: style.narrow,
      cellClass: style.publish,
      cell: (a) => (
        <div className={style.publish_inner}>
          <Toggle isActive={a.publish} disable />
        </div>
      ),
    },
    {
      key: 'created',
      header: t('manage.table.createdAt'),
      sortable: true,
      sortValue: (a) => new Date(a.created).getTime(),
      className: style.datetime,
      cell: (a) => formatDatetime(a.created),
    },
  ]

  return (
    <Main
      title="Advertise"
      type="table"
      toast={toast}
      isFooter={false}
      button={
        <div className={style.header_actions}>
          {selectedKeys.size > 0 && (
            <>
              <span className={style.selected_count}>{t('manage.header.selected', { count: selectedKeys.size })}</span>
              <Button color="red" size="s" name={t('manage.header.bulkDelete')} onClick={handleModal} />
            </>
          )}
          <Button color="blue" size="s" name={t('manage.title')} onClick={() => router.push('/manage')} />
          <Button color="green" size="s" name={t('manage.button.new')} disabled={isLimitReached} onClick={handleCreate} />
        </div>
      }
    >
      <ManageTable
        table={{ datas: items, columns, rowKey: (a) => a.ulid }}
        selection={{ keys: selectedKeys, onChange: setSelectedKeys }}
        pagination={{ current: currentPage, total: totalPages, onChange: handlePage }}
        deletion={{ open: isModal, loading, onClose: handleModal, onAction: handleDeleteSubmit }}
      />
    </Main>
  )
}
