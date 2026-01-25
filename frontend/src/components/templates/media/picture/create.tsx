import { useState, ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { Channel } from 'types/internal/channle'
import { PictureIn } from 'types/internal/media'
import { Option } from 'types/internal/other'
import { postPictureCreate } from 'api/internal/media/create'
import { FetchError } from 'utils/constants/enum'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import Select from 'components/parts/Input/Select'
import Textarea from 'components/parts/Input/Textarea'
import VStack from 'components/parts/Stack/Vertical'

interface Props {
  channels: Channel[]
}

export default function PictureCreate(props: Props): React.JSX.Element {
  const { channels } = props

  const channelUlid = channels.find((c) => c.isDefault)?.ulid ?? ''
  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))

  const router = useRouter()
  const { toast, handleToast } = useToast()
  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const [values, setValues] = useState<PictureIn>({ channelUlid, title: '', content: '' })

  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })

  const handleForm = async () => {
    const { channelUlid, title, content, image } = values
    if (!isRequiredCheck({ channelUlid, title, content, image })) return
    handleLoading(true)
    const ret = await postPictureCreate(values)
    if (ret.isErr()) {
      handleToast(FetchError.Post, true)
      handleLoading(false)
      return
    }
    router.push(`/media/picture/${ret.value.ulid}`)
    handleLoading(false)
  }

  return (
    <Main title="Picture" type="table" toast={toast} button={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <form method="POST" action="">
        <VStack gap="8">
          <Select label="チャンネル" name="channelUlid" value={values.channelUlid} options={channelOptions} onChange={handleSelect} />
          <Input label="タイトル" name="title" required={isRequired} onChange={handleInput} />
          <Textarea label="内容" name="content" required={isRequired} onChange={handleText} />
          <InputFile label="画像" accept="image/*" required={isRequired} onChange={handleFile} />
        </VStack>
      </form>
    </Main>
  )
}
