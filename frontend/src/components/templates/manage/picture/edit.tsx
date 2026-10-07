import { useState, ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import { Category } from 'types/internal/category'
import { Channel } from 'types/internal/channel'
import { PictureUpdateIn } from 'types/internal/media/input'
import { Picture } from 'types/internal/media/output'
import { Option } from 'types/internal/other'
import { putManagePicture } from 'api/internal/manage/update'
import { Fetch, FetchError } from 'utils/constants/enum'
import { useApiError } from 'components/hooks/useApiError'
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
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'

interface Props {
  data: Picture
  channels: Channel[]
  categories: Category[]
}

export default function ManagePictureEdit(props: Props): React.JSX.Element {
  const { data, channels, categories } = props

  const router = useRouter()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const { handleError } = useApiError({ handleToast })
  const [values, setValues] = useState<PictureUpdateIn>({ categoryUlid: data.categoryUlid, title: data.title, content: data.content, publish: data.publish })

  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))
  const categoryOptions: Option[] = [{ label: t('manage.form.unselected'), value: '' }, ...categories.map((c) => ({ label: c.jpName, value: c.ulid }))]

  const handleBack = () => router.push('/manage/picture')
  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })

  const handleForm = async () => {
    const { categoryUlid, title, content } = values
    if (!validate({ categoryUlid, title, content })) return
    handleLoading(true)
    const ret = await putManagePicture(data.ulid, values)
    handleLoading(false)
    if (ret.isErr()) {
      handleError(FetchError.Put, ret.error.message)
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
    <Main title="Picture" type="table" toast={toast} isFooter={false} button={button}>
      <form method="POST" action="" encType="multipart/form-data">
        <VStack gap="8">
          <ToggleCard label={t('manage.form.publish')} isActive={values.publish} onClick={handlePublish} />
          <SelectBox label={t('manage.form.channel')} name="channelUlid" value={data.channel.ulid} options={channelOptions} disabled />
          <SelectBox label={t('manage.form.category')} name="categoryUlid" value={values.categoryUlid} options={categoryOptions} required error={error} onChange={handleSelect} />
          <Input label={t('manage.form.title')} name="title" value={values.title} required error={error} onChange={handleInput} />
          <Textarea label={t('manage.form.content')} name="content" value={values.content} required error={error} onChange={handleText} />
          <InputFile label={t('manage.form.image')} accept="image/*" required error={error} onChange={handleFile} />
        </VStack>
      </form>
    </Main>
  )
}
