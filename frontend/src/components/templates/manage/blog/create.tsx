import { useState, ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import { toErrorMessage } from 'lib/error'
import { Category } from 'types/internal/category'
import { Channel } from 'types/internal/channel'
import { BlogIn } from 'types/internal/media/input'
import { Option } from 'types/internal/other'
import { postBlogCreate } from 'api/internal/manage/create'
import { FetchError } from 'utils/constants/enum'
import { useLoading } from 'components/hooks/useLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import SelectBox from 'components/parts/Input/SelectBox'
import Textarea from 'components/parts/Input/Textarea'
import ToggleCard from 'components/parts/Input/ToggleCard'
import Modal from 'components/parts/Modal'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import BlogArticle from 'components/widgets/BlogArticle'
import TextEditor from 'components/widgets/TextEditor'

interface Props {
  channels: Channel[]
  categories: Category[]
}

export default function BlogCreate(props: Props): React.JSX.Element {
  const { channels, categories } = props

  const router = useRouter()
  const { t } = useTranslation()

  const channelUlid = channels.find((c) => c.isDefault)!.ulid
  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))
  const categoryOptions: Option[] = [{ label: t('manage.form.unselected'), value: '' }, ...categories.map((c) => ({ label: c.jpName, value: c.ulid }))]

  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const [values, setValues] = useState<BlogIn>({ channelUlid, categoryUlid: '', publish: true, title: '', content: '', richtext: '', isPromotion: false })
  const [isModal, setIsModal] = useState<boolean>(false)

  const handleModal = () => setIsModal(!isModal)
  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handlePromotion = () => setValues({ ...values, isPromotion: !values.isPromotion })
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })

  const handleRichtext = (html: string) => {
    const richtext = html.trim() === '<p></p>' ? '' : html.trim()
    setValues({ ...values, richtext })
  }

  const handleForm = async () => {
    const { channelUlid, categoryUlid, title, content, richtext, image } = values
    if (!validate({ channelUlid, categoryUlid, title, content, richtext, image })) return
    handleLoading(true)
    const ret = await postBlogCreate(values)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(toErrorMessage(ret.error, FetchError.Post), true)
      return
    }
    router.push({ pathname: '/manage/blog', query: { channel: channelUlid } })
  }

  const button = (
    <HStack gap="4">
      <Button color="green" size="s" name={t('manage.button.create')} loading={loading} onClick={handleForm} />
      <Button color="purple" size="s" name={t('manage.button.preview')} onClick={handleModal} />
    </HStack>
  )

  return (
    <Main title="Blog" type="table" toast={toast} isFooter={false} button={button}>
      <form method="POST" action="">
        <VStack gap="8">
          <ToggleCard label={t('manage.form.publish')} isActive={values.publish} onClick={handlePublish} />
          <ToggleCard label={t('manage.form.promotion')} isActive={values.isPromotion} onClick={handlePromotion} />
          <SelectBox label={t('manage.form.channel')} name="channelUlid" value={values.channelUlid} options={channelOptions} onChange={handleSelect} />
          <SelectBox label={t('manage.form.category')} name="categoryUlid" value={values.categoryUlid} options={categoryOptions} required error={error} onChange={handleSelect} />
          <Input label={t('manage.form.title')} name="title" required error={error} onChange={handleInput} />
          <Textarea label={t('manage.form.content')} name="content" required error={error} onChange={handleText} />
          <InputFile label={t('manage.form.thumbnail')} accept="image/*" required error={error} onChange={handleFile} />
          <TextEditor label={t('manage.form.richtext')} value={values.richtext} required error={error} onChange={handleRichtext} />
        </VStack>
      </form>
      <Modal open={isModal} onClose={handleModal} title={t('manage.button.preview')} size="l">
        <BlogArticle richtext={values.richtext} isPromotion={values.isPromotion} />
      </Modal>
    </Main>
  )
}
