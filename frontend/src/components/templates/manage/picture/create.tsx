import { useState, ChangeEvent } from 'react'
import { Category } from 'types/internal/category'
import { Channel } from 'types/internal/channel'
import { PictureIn } from 'types/internal/media/input'
import { Option } from 'types/internal/other'
import { postPictureCreate } from 'api/internal/manage/create'
import { FetchError } from 'utils/constants/enum'
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
import VStack from 'components/parts/Stack/Vertical'

interface Props {
  channels: Channel[]
  categories: Category[]
}

export default function PictureCreate(props: Props): React.JSX.Element {
  const { channels, categories } = props

  const channelUlid = channels.find((c) => c.isDefault)!.ulid
  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))
  const categoryOptions: Option[] = [{ label: '未選択', value: '' }, ...categories.map((c) => ({ label: c.jpName, value: c.ulid }))]

  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const { toast, handleToast } = useToast()
  const [values, setValues] = useState<PictureIn>({ channelUlid, categoryUlid: '', publish: true, title: '', content: '' })

  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })

  const handleForm = async () => {
    const { channelUlid, categoryUlid, title, content, image } = values
    if (!isRequiredCheck({ channelUlid, categoryUlid, title, content, image })) return
    handleLoading(true)
    const ret = await postPictureCreate(values)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(FetchError.Post, true)
      return
    }
    setValues({ channelUlid, categoryUlid: '', publish: true, title: '', content: '' })
    handleToast('作成しました', false)
  }

  return (
    <Main title="Picture" type="table" toast={toast} isFooter={false} button={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <form method="POST" action="">
        <VStack gap="8">
          <ToggleCard label="公開する" isActive={values.publish} onClick={handlePublish} />
          <SelectBox label="チャンネル" name="channelUlid" value={values.channelUlid} options={channelOptions} onChange={handleSelect} />
          <SelectBox label="カテゴリー" name="categoryUlid" value={values.categoryUlid} options={categoryOptions} required={isRequired} onChange={handleSelect} />
          <Input label="タイトル" name="title" required={isRequired} onChange={handleInput} />
          <Textarea label="内容" name="content" required={isRequired} onChange={handleText} />
          <InputFile label="画像" accept="image/*" required={isRequired} onChange={handleFile} />
        </VStack>
      </form>
    </Main>
  )
}
