import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQueryClient } from '@tanstack/react-query'
import { errorMessage } from 'lib/error'
import { queryKeys } from 'lib/query/keys'
import { Option } from 'types/internal/other'
import { SeriesDetail, SeriesItem } from 'types/internal/series'
import { deleteManageSeries, putManageSeries } from 'api/internal/manage/series'
import { Fetch, FetchError } from 'utils/constants/enum'
import cx from 'utils/functions/cx'
import { useLoading } from 'components/hooks/useLoading'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import IconCross from 'components/parts/Icon/Cross'
import IconGrip from 'components/parts/Icon/Grip'
import Input from 'components/parts/Input'
import SelectBox from 'components/parts/Input/SelectBox'
import HStack from 'components/parts/Stack/Horizontal'
import DeleteModal from 'components/widgets/Modal/Delete'
import style from './Edit.module.scss'

interface Props {
  data: SeriesDetail
}

export default function ManageSeriesEdit(props: Props): React.JSX.Element {
  const { data } = props

  const router = useRouter()
  const queryClient = useQueryClient()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { toast, handleToast } = useToast()
  const [isModal, setIsModal] = useState<boolean>(false)
  const [title, setTitle] = useState<string>(data.title)
  const [items, setItems] = useState<SeriesItem[]>(data.items)
  const [candidates, setCandidates] = useState<SeriesItem[]>(data.candidates)
  const [selectedUlid, setSelectedUlid] = useState<string>(data.candidates[0]?.ulid ?? '')
  const [dragIndex, setDragIndex] = useState<number | null>(null)
  const [dragOverIndex, setDragOverIndex] = useState<number | null>(null)

  const candidateOptions: Option[] = candidates.map((c) => ({ label: c.title, value: c.ulid }))

  const handleModal = () => setIsModal(!isModal)
  const handleBack = () => router.push({ pathname: '/manage/series', query: { channel: data.channelUlid } })
  const handleTitle = (e: ChangeEvent<HTMLInputElement>) => setTitle(e.target.value)
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setSelectedUlid(e.target.value)

  const handleAdd = () => {
    const item = candidates.find((c) => c.ulid === selectedUlid)
    if (!item) return
    const rest = candidates.filter((c) => c.ulid !== selectedUlid)
    setItems([...items, item])
    setCandidates(rest)
    setSelectedUlid(rest[0]?.ulid ?? '')
  }

  const handleRemove = (index: number) => {
    const item = items[index]
    if (!item) return
    setItems(items.filter((_, i) => i !== index))
    setCandidates([...candidates, item])
    if (selectedUlid === '') setSelectedUlid(item.ulid)
  }

  const handleDragStart = (index: number) => setDragIndex(index)

  const handleDrag = (e: React.DragEvent, index: number | null = null) => {
    e.preventDefault()
    setDragOverIndex(index)
  }

  const handleDrop = (index: number) => {
    if (dragIndex === null || dragIndex === index) return
    const newItems = [...items]
    const removed = newItems.splice(dragIndex, 1)
    if (removed[0] === undefined) return
    newItems.splice(index, 0, removed[0])
    setItems(newItems)
  }

  const handleDragEnd = () => {
    setDragIndex(null)
    setDragOverIndex(null)
  }

  const handleSave = async () => {
    handleLoading(true)
    const ret = await putManageSeries(data.ulid, { title, mediaUlids: items.map((item) => item.ulid) })
    handleLoading(false)
    if (ret.isErr()) return handleToast(errorMessage(ret.error, FetchError.Put), true)
    await queryClient.invalidateQueries({ queryKey: queryKeys.manageSeriesAll })
    handleToast(Fetch.Save, false)
  }

  const handleDelete = async () => {
    handleLoading(true)
    const ret = await deleteManageSeries(data.ulid)
    handleLoading(false)
    if (ret.isErr()) return handleToast(errorMessage(ret.error, FetchError.Delete), true)
    await queryClient.invalidateQueries({ queryKey: queryKeys.manageSeriesAll })
    handleBack()
  }

  const button = (
    <HStack gap="4">
      <Button color="green" size="s" name={t('manage.button.save')} loading={loading} disabled={title.trim() === ''} onClick={handleSave} />
      <Button color="red" size="s" name={t('action.delete')} disabled={loading} onClick={handleModal} />
      <Button color="blue" size="s" name={t('status.back')} onClick={handleBack} />
    </HStack>
  )

  return (
    <Main title="Series" type="table" toast={toast} isFooter={false} button={button}>
      <div className={style.edit}>
        <span className={style.media_type}>{data.mediaType}</span>
        <Input label={t('manage.form.title')} value={title} maxLength={100} required onChange={handleTitle} />

        <div className={style.add}>
          <SelectBox label={t('manage.series.candidate')} value={selectedUlid} options={candidateOptions} className={style.add_select} onChange={handleSelect} />
          <Button color="blue" size="s" name={t('action.add')} disabled={selectedUlid === ''} onClick={handleAdd} />
        </div>

        {items.length > 0 ? (
          <ol className={style.list}>
            {items.map((item, index) => (
              <li
                key={item.ulid}
                draggable
                className={cx(style.item, dragIndex === index && style.dragging, dragOverIndex === index && style.drag_over)}
                onDragStart={() => handleDragStart(index)}
                onDragOver={(e) => handleDrag(e, index)}
                onDragLeave={(e) => handleDrag(e)}
                onDrop={() => handleDrop(index)}
                onDragEnd={handleDragEnd}
              >
                <IconGrip size="14" className={style.grip} />
                <span className={style.index}>{index + 1}</span>
                <span className={style.title}>{item.title}</span>
                {!item.publish && <span className={style.private}>{t('manage.series.private')}</span>}
                <button type="button" title={t('action.delete')} className={style.remove} onClick={() => handleRemove(index)}>
                  <IconCross size="18" />
                </button>
              </li>
            ))}
          </ol>
        ) : (
          <p className={style.empty}>{t('manage.series.empty')}</p>
        )}
      </div>

      <DeleteModal open={isModal} title={t('manage.series.deleteTitle')} content={t('manage.series.deleteConfirm', { title: data.title })} loading={loading} onClose={handleModal} onAction={handleDelete} />
    </Main>
  )
}
