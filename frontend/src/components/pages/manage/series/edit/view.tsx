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
import { useDragSort } from 'components/hooks/useDragSort'
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
import VStack from 'components/parts/Stack/Vertical'
import DeleteModal from 'components/widgets/Modal/Delete'
import style from './Edit.module.scss'
import formStyle from '../../Form.module.scss'

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
  const [search, setSearch] = useState<string>('')
  const [selectedUlid, setSelectedUlid] = useState<string>('')
  const { dragIndex, dragOverIndex, dragProps } = useDragSort(items, setItems)

  const mediaTypeOptions: Option[] = [{ label: data.mediaType, value: data.mediaType }]
  const filtered = candidates.filter((c) => c.title.toLowerCase().includes(search.trim().toLowerCase()))
  const selected = filtered.find((c) => c.ulid === selectedUlid) ?? filtered[0]
  const candidateOptions: Option[] = filtered.map((c) => ({ label: c.title, value: c.ulid }))

  const handleModal = () => setIsModal(!isModal)
  const handleBack = () => router.push({ pathname: '/manage/series', query: { channel: data.channelUlid } })
  const handleTitle = (e: ChangeEvent<HTMLInputElement>) => setTitle(e.target.value)
  const handleSearch = (e: ChangeEvent<HTMLInputElement>) => setSearch(e.target.value)
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setSelectedUlid(e.target.value)

  const handleAdd = () => {
    if (!selected) return
    setItems([...items, selected])
    setCandidates(candidates.filter((c) => c.ulid !== selected.ulid))
    setSelectedUlid('')
  }

  const handleRemove = (index: number) => {
    const item = items[index]
    if (!item) return
    setItems(items.filter((_, i) => i !== index))
    setCandidates([...candidates, item])
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
      <form className={formStyle.form}>
        <VStack gap="8">
          <SelectBox label={t('manage.series.mediaType')} value={data.mediaType} options={mediaTypeOptions} disabled />
          <Input label={t('manage.form.title')} value={title} maxLength={100} required onChange={handleTitle} />
          <div className={style.add}>
            <Input label={t('manage.series.candidate')} value={search} placeholder={t('manage.series.search')} className={style.add_select} onChange={handleSearch} />
            <SelectBox value={selected?.ulid ?? ''} options={candidateOptions} className={style.add_select} onChange={handleSelect} />
            <Button color="blue" size="s" name={t('action.add')} disabled={!selected} onClick={handleAdd} />
          </div>
          <div className={style.posts}>
            <span className={style.label}>{t('manage.series.posts')}</span>
            {items.length > 0 ? (
              <ol className={style.list}>
                {items.map((item, index) => (
                  <li
                    key={item.ulid}
                    className={cx(style.item, dragIndex === index && style.dragging, dragOverIndex === index && style.drag_over)}
                    {...dragProps(index)}
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
        </VStack>
      </form>

      <DeleteModal open={isModal} title={t('manage.series.deleteTitle')} content={t('manage.series.deleteConfirm', { title: data.title })} loading={loading} onClose={handleModal} onAction={handleDelete} />
    </Main>
  )
}
