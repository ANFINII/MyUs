import { useState, ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { Channel } from 'types/internal/channle'
import { VideoIn } from 'types/internal/media'
import { Option } from 'types/internal/other'
import { postVideoCreate } from 'api/internal/media/create'
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
import VStack from 'components/parts/Stack/Vertical'

interface Props {
  channels: Channel[]
}

export default function VideoCreate(props: Props): React.JSX.Element {
  const { channels } = props

  const channelUlid = channels.find((c) => c.isDefault)?.ulid ?? ''
  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))

  const router = useRouter()
  const { toast, handleToast } = useToast()
  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const [values, setValues] = useState<VideoIn>({ channelUlid, title: '', content: '' })

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
    if (ret.isErr()) {
      handleToast(FetchError.Post, true)
      handleLoading(false)
      return
    }
    router.push(`/media/video/${ret.value.ulid}`)
    handleLoading(false)
  }

  return (
    <Main title="Video" type="table" toast={toast} button={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <form method="POST" action="" encType="multipart/form-data">
        <VStack gap="8">
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
