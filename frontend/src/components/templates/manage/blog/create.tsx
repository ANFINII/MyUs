import { useState, ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import { Category } from 'types/internal/category'
import { Channel } from 'types/internal/channel'
import { BlogIn } from 'types/internal/media/input'
import { Option } from 'types/internal/other'
import { postBlogCreate } from 'api/internal/manage/create'
import { Fetch, FetchError } from 'utils/constants/enum'
import { useLoading } from 'components/hooks/useLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import SelectBox from 'components/parts/Input/SelectBox'
import Textarea from 'components/parts/Input/Textarea'
import ToggleCard from 'components/parts/Input/ToggleCard'
import VStack from 'components/parts/Stack/Vertical'
import TextEditor from 'components/widgets/TextEditor'

interface Props {
  channels: Channel[]
  categories: Category[]
}

export default function BlogCreate(props: Props): React.JSX.Element {
  const { channels, categories } = props

  const { t } = useTranslation()

  const channelUlid = channels.find((c) => c.isDefault)!.ulid
  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))
  const categoryOptions: Option[] = [{ label: t('manage.form.unselected'), value: '' }, ...categories.map((c) => ({ label: c.jpName, value: c.ulid }))]

  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const [values, setValues] = useState<BlogIn>({ channelUlid, categoryUlid: '', publish: true, title: '', content: '', richtext: '' })

  const handlePublish = () => setValues({ ...values, publish: !values.publish })
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
      handleToast(FetchError.Post, true)
      return
    }
    setValues({ channelUlid, categoryUlid: '', publish: true, title: '', content: '', richtext: '' })
    handleToast(Fetch.Create, false)
  }

  return (
    <Main
      title="Blog"
      type="table"
      toast={toast}
      isFooter={false}
      button={<Button color="green" size="s" name={t('manage.button.create')} loading={loading} onClick={handleForm} />}
    >
      <form method="POST" action="">
        <VStack gap="8">
          <ToggleCard label={t('manage.form.publish')} isActive={values.publish} onClick={handlePublish} />
          <SelectBox label={t('manage.form.channel')} name="channelUlid" value={values.channelUlid} options={channelOptions} onChange={handleSelect} />
          <SelectBox label={t('manage.form.category')} name="categoryUlid" value={values.categoryUlid} options={categoryOptions} required error={error} onChange={handleSelect} />
          <Input label={t('manage.form.title')} name="title" required error={error} onChange={handleInput} />
          <Textarea label={t('manage.form.content')} name="content" required error={error} onChange={handleText} />
          <InputFile label={t('manage.form.thumbnail')} accept="image/*" required error={error} onChange={handleFile} />
          <TextEditor label={t('manage.form.richtext')} value={values.richtext} required error={error} onChange={handleRichtext} />
        </VStack>
      </form>
    </Main>
  )
}
