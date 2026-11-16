import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { errorMessage } from 'lib/error'
import { Channel } from 'types/internal/channel'
import { Option } from 'types/internal/other'
import { Series, SeriesList } from 'types/internal/series'
import { postManageSeries } from 'api/internal/manage/series'
import { FetchError, MediaType } from 'utils/constants/enum'
import { useLoading } from 'components/hooks/useLoading'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import DataTable, { Column } from 'components/parts/DataTable'
import Input from 'components/parts/Input'
import SelectBox from 'components/parts/Input/SelectBox'
import Modal from 'components/parts/Modal'
import HStack from 'components/parts/Stack/Horizontal'
import style from './Series.module.scss'

const mediaTypeOptions: Option[] = Object.values(MediaType).map((type) => ({ label: type, value: type }))

interface Props {
  channels: Channel[]
  data: SeriesList
  channel: string
}

export default function ManageSeriesList(props: Props): React.JSX.Element {
  const { channels, data, channel } = props

  const router = useRouter()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { toast, handleToast } = useToast()
  const [isModal, setIsModal] = useState<boolean>(false)
  const [mediaType, setMediaType] = useState<MediaType>(MediaType.Video)
  const [title, setTitle] = useState<string>('')

  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))

  const handleModal = () => setIsModal(!isModal)
  const handleEdit = (ulid: string) => router.push(`/manage/series/${ulid}`)
  const handleChannel = (e: ChangeEvent<HTMLSelectElement>) => router.push({ pathname: router.pathname, query: { channel: e.target.value } })
  const handleMediaType = (e: ChangeEvent<HTMLSelectElement>) => setMediaType(Object.values(MediaType).find((type) => type === e.target.value) ?? MediaType.Video)
  const handleTitle = (e: ChangeEvent<HTMLInputElement>) => setTitle(e.target.value)

  const handleCreate = async () => {
    handleLoading(true)
    const ret = await postManageSeries({ channelUlid: channel, mediaType, title })
    handleLoading(false)
    if (ret.isErr()) return handleToast(errorMessage(ret.error, FetchError.Post), true)
    router.push(`/manage/series/${ret.value.ulid}`)
  }

  const columns: Column<Series>[] = [
    {
      key: 'title',
      header: t('manage.table.title'),
      sortable: true,
      sortValue: (s) => s.title,
      cell: (s) => (
        <a className={style.title_link} onClick={() => handleEdit(s.ulid)}>
          {s.title}
        </a>
      ),
    },
    {
      key: 'mediaType',
      header: t('manage.series.mediaType'),
      sortable: true,
      sortValue: (s) => s.mediaType,
      className: style.normal,
      cell: (s) => s.mediaType,
    },
    {
      key: 'count',
      header: t('manage.series.count'),
      align: 'right',
      sortable: true,
      sortValue: (s) => s.count,
      className: style.normal,
      cellClass: style.number,
      cell: (s) => s.count,
    },
  ]

  const button = (
    <HStack gap="4">
      <Button color="blue" size="s" name={t('manage.title')} onClick={() => router.push('/manage')} />
      <Button color="green" size="s" name={t('manage.series.new')} onClick={handleModal} />
      <SelectBox value={channel} options={channelOptions} className={style.select_box} onChange={handleChannel} />
    </HStack>
  )

  return (
    <Main title="Series" type="table" toast={toast} isFooter={false} button={button}>
      <DataTable datas={data.items} columns={columns} rowKey={(s) => s.ulid} />

      <Modal
        open={isModal}
        onClose={handleModal}
        title={t('manage.series.new')}
        size="s"
        actions={[
          { name: t('action.cancel'), color: 'white', disabled: loading, onClick: handleModal },
          { name: t('manage.button.create'), color: 'blue', loading, disabled: title.trim() === '', onClick: handleCreate },
        ]}
      >
        <div className={style.form}>
          <SelectBox label={t('manage.series.mediaType')} value={mediaType} options={mediaTypeOptions} onChange={handleMediaType} />
          <Input label={t('manage.form.title')} value={title} maxLength={100} onChange={handleTitle} />
        </div>
      </Modal>
    </Main>
  )
}
