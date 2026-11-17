import { useState, ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import { errorMessage } from 'lib/error'
import { Category } from 'types/internal/category'
import { Channel } from 'types/internal/channel'
import { ComicIn } from 'types/internal/media/input'
import { postComicCreate } from 'api/internal/manage/create'
import { FetchError } from 'utils/constants/enum'
import { datetimeLocal, datetimeISO } from 'utils/functions/datetime'
import { previewUrl } from 'utils/functions/file'
import { useLoading } from 'components/hooks/useLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import DatePicker from 'components/parts/Input/DatePicker'
import InputFile from 'components/parts/Input/File'
import SelectBox from 'components/parts/Input/SelectBox'
import Textarea from 'components/parts/Input/Textarea'
import ToggleCard from 'components/parts/Input/ToggleCard'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import ComicModal from 'components/widgets/Modal/Comic'
import style from '../../Form.module.scss'

interface Props {
  channels: Channel[]
  categories: Category[]
}

export default function ComicCreate(props: Props): React.JSX.Element {
  const { channels, categories } = props

  const channelUlid = channels.find((c) => c.isDefault)!.ulid

  const router = useRouter()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const [isModal, setIsModal] = useState<boolean>(false)
  const [previewPages, setPreviewPages] = useState<string[]>([])
  const [values, setValues] = useState<ComicIn>({ channelUlid, categoryUlid: '', publish: true, publishAt: datetimeISO(), title: '', content: '' })

  const channelOptions = channels.map((c) => ({ label: c.name, value: c.ulid }))
  const categoryOptions = [{ label: t('manage.form.unselected'), value: '' }, ...categories.map((c) => ({ label: c.jpName, value: c.ulid }))]

  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleFile = (file: File) => setValues({ ...values, image: file })
  const handleMultiFile = (files: File[]) => setValues({ ...values, pages: files })
  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handlePublishAt = (publishAt: string) => setValues({ ...values, publishAt: datetimeISO(publishAt) })

  const handleModal = () => {
    if (isModal) {
      previewPages.forEach((url) => URL.revokeObjectURL(url))
      setPreviewPages([])
    } else {
      const { image, pages = [] } = values
      const files = image ? [image, ...pages] : pages
      setPreviewPages(files.map((file) => previewUrl(file)))
    }
    setIsModal(!isModal)
  }

  const handleForm = async () => {
    const { channelUlid, categoryUlid, title, content, image, pages } = values
    if (!validate({ channelUlid, categoryUlid, title, content, image, pages })) return
    handleLoading(true)
    const ret = await postComicCreate(values)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(errorMessage(ret.error, FetchError.Post), true)
      return
    }
    router.push({ pathname: '/manage/comic', query: { channel: channelUlid } })
  }

  const button = (
    <HStack gap="4">
      <Button color="purple" size="s" name={t('manage.button.preview')} onClick={handleModal} />
      <Button color="green" size="s" name={t('manage.button.create')} loading={loading} onClick={handleForm} />
    </HStack>
  )

  return (
    <Main title="Comic" type="table" toast={toast} isFooter={false} button={button}>
      <form className={style.form} method="POST" action="" encType="multipart/form-data">
        <VStack gap="8">
          <ToggleCard label={t('manage.form.publish')} isActive={values.publish} onClick={handlePublish} />
          <DatePicker label={t('manage.form.publishAt')} name="publishAt" value={datetimeLocal(values.publishAt)} onChange={handlePublishAt} isTime />
          <SelectBox label={t('manage.form.channel')} name="channelUlid" value={values.channelUlid} options={channelOptions} onChange={handleSelect} />
          <SelectBox label={t('manage.form.category')} name="categoryUlid" value={values.categoryUlid} options={categoryOptions} required error={error} onChange={handleSelect} />
          <Input label={t('manage.form.title')} name="title" maxLength={100} required error={error} onChange={handleInput} />
          <Textarea label={t('manage.form.content')} name="content" required error={error} onChange={handleText} />
          <InputFile label={t('manage.form.thumbnail')} accept="image/*" required error={error} onChange={handleFile} />
          <InputFile label={t('manage.form.pages')} accept="image/*" required error={error} onMultiChange={handleMultiFile} />
        </VStack>
      </form>
      <ComicModal open={isModal} onClose={handleModal} pages={previewPages} />
    </Main>
  )
}
