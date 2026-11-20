import { useState, ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import { errorMessage } from 'lib/error'
import { Category } from 'types/internal/category'
import { Channel } from 'types/internal/channel'
import { AudioUpdateIn } from 'types/internal/media/input'
import { Audio } from 'types/internal/media/output'
import { PaymentSellerOut } from 'types/internal/payment'
import { putManageAudio } from 'api/internal/manage/update'
import { Fetch, FetchError } from 'utils/constants/enum'
import { MEDIA_TITLE_MAX } from 'utils/functions/common'
import { datetimeLocal, datetimeISO } from 'utils/functions/datetime'
import { previewUrl } from 'utils/functions/file'
import { useLoading } from 'components/hooks/useLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import IconInfo from 'components/parts/Icon/Info'
import Input from 'components/parts/Input'
import DatePicker from 'components/parts/Input/DatePicker'
import InputFile from 'components/parts/Input/File'
import SelectBox from 'components/parts/Input/SelectBox'
import Textarea from 'components/parts/Input/Textarea'
import ToggleCard from 'components/parts/Input/ToggleCard'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import style from '../../Form.module.scss'
import HiresSale from '../HiresSale'
import LyricEditor from '../LyricEditor'

interface Props {
  channels: Channel[]
  categories: Category[]
  seller: PaymentSellerOut
  data: Audio
}

export default function ManageAudioEdit(props: Props): React.JSX.Element {
  const { channels, categories, seller, data } = props
  const { categoryUlid, title, content, lyric, publish, publishAt } = data

  const router = useRouter()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const [isModal, setIsModal] = useState<boolean>(false)
  const [audioUrl, setAudioUrl] = useState<string>('')
  const [values, setValues] = useState<AudioUpdateIn>({ categoryUlid, title, content, lyric, publish, publishAt: datetimeISO(publishAt) })

  const channelOptions = channels.map((c) => ({ label: c.name, value: c.ulid }))
  const categoryOptions = [{ label: t('manage.form.unselected'), value: '' }, ...categories.map((c) => ({ label: c.jpName, value: c.ulid }))]

  const handleBack = () => router.push('/manage/audio')
  const handleModal = () => setIsModal(!isModal)
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleImage = (file: File) => setValues({ ...values, image: file })
  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handlePublishAt = (publishAt: string) => setValues({ ...values, publishAt: datetimeISO(publishAt) })

  const handleFile = (file: File) => {
    setValues({ ...values, audio: file })
    setAudioUrl(previewUrl(file, audioUrl))
  }

  const handleLyric = (lyric: string) => {
    setValues({ ...values, lyric })
    setIsModal(false)
  }

  const handleForm = async () => {
    const { categoryUlid, title, content } = values
    if (!validate({ categoryUlid, title, content })) return
    handleLoading(true)
    const ret = await putManageAudio(data.ulid, values)
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
    <Main title="Audio" type="table" size="l" toast={toast} isFooter={false} button={button}>
      <form method="POST" action="" encType="multipart/form-data">
        <VStack gap="8">
          <ToggleCard label={t('manage.form.publish')} isActive={values.publish} onClick={handlePublish} />
          <DatePicker label={t('manage.form.publishAt')} name="publishAt" value={datetimeLocal(values.publishAt)} onChange={handlePublishAt} isTime />
          <SelectBox label={t('manage.form.channel')} name="channelUlid" value={data.channel.ulid} options={channelOptions} disabled />
          <SelectBox label={t('manage.form.category')} name="categoryUlid" value={values.categoryUlid} options={categoryOptions} required error={error} onChange={handleSelect} />
          <Input label={t('manage.form.title')} name="title" maxLength={MEDIA_TITLE_MAX} value={values.title} required error={error} onChange={handleInput} />
          <Textarea label={t('manage.form.content')} name="content" value={values.content} required error={error} onChange={handleText} />
          <Textarea label={t('manage.form.lyric')} name="lyric" className={style.lyric} value={values.lyric} onChange={handleText} />
          <div className={style.lyric_hint}>
            <IconInfo size="14" className={style.lyric_hint_icon} />
            <span>{t('manage.form.lyricHint')}</span>
            <Button color="purple" size="s" name={t('manage.lyric.open')} className={style.lyric_hint_button} onClick={handleModal} />
          </div>
          <InputFile label={t('manage.form.thumbnail')} accept="image/*" onChange={handleImage} />
          <InputFile label={t('manage.form.audio')} accept="audio/*" onChange={handleFile} />
          <HiresSale ulid={data.ulid} seller={seller} hires={data.hires} product={data.product} handleToast={handleToast} />
        </VStack>
      </form>
      {isModal && <LyricEditor src={audioUrl || data.audio} lyric={values.lyric} onClose={handleModal} onApply={handleLyric} />}
    </Main>
  )
}
