import { useState, ChangeEvent } from 'react'
import { Channel } from 'types/internal/channel'
import { VideoIn } from 'types/internal/media/manage'
import { Option } from 'types/internal/other'
import { postVideoCreate } from 'api/internal/manage/create'
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
}

export default function VideoCreate(props: Props): React.JSX.Element {
  const { channels } = props

  const channelUlid = channels.find((c) => c.isDefault)?.ulid ?? ''
  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))

  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const { toast, handleToast } = useToast()
  const [formKey, setFormKey] = useState(0)
  const [values, setValues] = useState<VideoIn>({ channelUlid, publish: true, title: '', content: '' })

  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })
  const handleMovie = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, video: files })

  const handleForm = async () => {
    const { channelUlid, title, content, image, video } = values
    if (!isRequiredCheck({ channelUlid, title, content, image, video })) return
    handleLoading(true)
    const ret = await postVideoCreate(values)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(FetchError.Post, true)
      return
    }
    setValues({ channelUlid, publish: true, title: '', content: '' })
    setFormKey((prev) => prev + 1)
    handleToast('作成中です。完了まで時間がかかる場合があります', false)
  }

  return (
    <Main title="Video" type="table" toast={toast} isFooter={false} button={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <form key={formKey} method="POST" action="" encType="multipart/form-data">
        <VStack gap="8">
          <ToggleCard label="公開する" isActive={values.publish} onClick={handlePublish} />
          <SelectBox label="チャンネル" name="channelUlid" value={values.channelUlid} options={channelOptions} onChange={handleSelect} />
          <Input label="タイトル" name="title" required={isRequired} onChange={handleInput} />
          <Textarea label="内容" name="content" required={isRequired} onChange={handleText} />
          <InputFile label="サムネイル" accept="image/*" required={isRequired} onChange={handleFile} />
          <InputFile label="動画" accept="video/*" required={isRequired} onChange={handleMovie} />
        </VStack>
      </form>
    </Main>
  )
}
