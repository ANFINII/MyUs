import { useState, ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { Category } from 'types/internal/category'
import { Channel } from 'types/internal/channel'
import { PictureUpdateIn } from 'types/internal/media/input'
import { Picture } from 'types/internal/media/output'
import { Option } from 'types/internal/other'
import { putManagePicture } from 'api/internal/manage/update'
import { FetchError } from 'utils/constants/enum'
import { useApiError } from 'components/hooks/useApiError'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { useRequired } from 'components/hooks/useRequired'
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

  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))
  const categoryOptions: Option[] = [{ label: '未選択', value: '' }, ...categories.map((c) => ({ label: c.jpName, value: c.ulid }))]

  const router = useRouter()
  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const { toast, handleToast } = useToast()
  const { handleError } = useApiError({ handleToast })
  const [values, setValues] = useState<PictureUpdateIn>({ categoryUlid: data.categoryUlid, title: data.title, content: data.content, publish: data.publish })

  const handleBack = () => router.push('/manage/picture')
  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })

  const handleForm = async () => {
    const { categoryUlid, title, content } = values
    if (!isRequiredCheck({ categoryUlid, title, content })) return
    handleLoading(true)
    const ret = await putManagePicture(data.ulid, values)
    handleLoading(false)
    if (ret.isErr()) {
      handleError(FetchError.Put, ret.error.message)
      return
    }
    handleToast('保存しました', false)
  }

  const button = (
    <HStack gap="4">
      <Button color="green" size="s" name="保存する" loading={isLoading} onClick={handleForm} />
      <Button color="blue" size="s" name="戻る" onClick={handleBack} />
    </HStack>
  )

  return (
    <Main title="画像編集" type="table" toast={toast} isFooter={false} button={button}>
      <form method="POST" action="" encType="multipart/form-data">
        <VStack gap="8">
          <ToggleCard label="公開する" isActive={values.publish} onClick={handlePublish} />
          <SelectBox label="チャンネル" name="channelUlid" value={data.channel.ulid} options={channelOptions} disabled />
          <SelectBox label="カテゴリー" name="categoryUlid" value={values.categoryUlid} options={categoryOptions} required={isRequired} onChange={handleSelect} />
          <Input label="タイトル" name="title" value={values.title} required={isRequired} onChange={handleInput} />
          <Textarea label="内容" name="content" value={values.content} required={isRequired} onChange={handleText} />
          <InputFile label="画像" accept="image/*" onChange={handleFile} />
        </VStack>
      </form>
    </Main>
  )
}
