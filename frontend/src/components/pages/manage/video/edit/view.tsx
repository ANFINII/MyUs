import { useState, ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import { errorMessage } from 'lib/error'
import { Category } from 'types/internal/category'
import { Channel } from 'types/internal/channel'
import { VideoUpdateIn } from 'types/internal/media/input'
import { Video } from 'types/internal/media/output'
import { putManageVideo } from 'api/internal/manage/update'
import { EncodeStatus, Fetch, FetchError } from 'utils/constants/enum'
import { MEDIA_TITLE_MAX } from 'utils/functions/common'
import { datetimeLocal, datetimeISO } from 'utils/functions/datetime'
import { useLoading } from 'components/hooks/useLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Alert from 'components/parts/Alert'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import DatePicker from 'components/parts/Input/DatePicker'
import InputFile from 'components/parts/Input/File'
import SelectBox from 'components/parts/Input/SelectBox'
import Textarea from 'components/parts/Input/Textarea'
import ToggleCard from 'components/parts/Input/ToggleCard'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'

interface Props {
  channels: Channel[]
  categories: Category[]
  data: Video
}

export default function ManageVideoEdit(props: Props): React.JSX.Element {
  const { channels, categories, data } = props
  const { categoryUlid, title, content, publish, publishAt } = data

  const router = useRouter()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const [values, setValues] = useState<VideoUpdateIn>({ categoryUlid, title, content, publish, publishAt: datetimeISO(publishAt) })

  const isEncodeFailed = data.encodeStatus === EncodeStatus.Failed
  const channelOptions = channels.map((c) => ({ label: c.name, value: c.ulid }))
  const categoryOptions = [{ label: t('manage.form.unselected'), value: '' }, ...categories.map((c) => ({ label: c.jpName, value: c.ulid }))]

  const handleBack = () => router.push('/manage/video')
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleFile = (file: File) => setValues({ ...values, image: file })
  const handleMovie = (file: File) => setValues({ ...values, video: file })
  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handlePublishAt = (publishAt: string) => setValues({ ...values, publishAt: datetimeISO(publishAt) })

  const handleForm = async () => {
    const { categoryUlid, title, content, video } = values
    if (!validate(isEncodeFailed ? { categoryUlid, title, content, video } : { categoryUlid, title, content })) return
    handleLoading(true)
    const ret = await putManageVideo(data.ulid, values)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(errorMessage(ret.error, FetchError.Put), true)
      return
    }
    handleToast(Fetch.Save, false)
  }

  const button = (
    <HStack gap="4">
      <Button color="green" size="s" name={t('manage.button.save')} loading={loading} onClick={handleForm} />
      <Button color="blue" size="s" name={t('status.back')} onClick={handleBack} />
    </HStack>
  )

  return (
    <Main title="Video" type="table" size="xl" toast={toast} isFooter={false} button={button}>
      <form method="POST" action="" encType="multipart/form-data">
        <VStack gap="8">
          {isEncodeFailed && <Alert type="error">{t('manage.video.encodeFailedNotice')}</Alert>}
          <ToggleCard label={t('manage.form.publish')} isActive={values.publish} onClick={handlePublish} />
          <DatePicker label={t('manage.form.publishAt')} name="publishAt" value={datetimeLocal(values.publishAt)} onChange={handlePublishAt} isTime />
          <SelectBox label={t('manage.form.channel')} name="channelUlid" value={data.channel.ulid} options={channelOptions} disabled />
          <SelectBox label={t('manage.form.category')} name="categoryUlid" value={values.categoryUlid} options={categoryOptions} required error={error} onChange={handleSelect} />
          <Input label={t('manage.form.title')} name="title" maxLength={MEDIA_TITLE_MAX} value={values.title} required error={error} onChange={handleInput} />
          <Textarea label={t('manage.form.content')} name="content" value={values.content} required error={error} onChange={handleText} />
          <InputFile label={t('manage.form.thumbnail')} accept="image/*" required error={error} onChange={handleFile} />
          {isEncodeFailed && <InputFile label={t('manage.form.video')} accept="video/*" required error={error} onChange={handleMovie} />}
        </VStack>
      </form>
    </Main>
  )
}
