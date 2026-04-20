import { useState, ChangeEvent } from 'react'
import dynamic from 'next/dynamic'
import { useRouter } from 'next/router'
import { Channel } from 'types/internal/channel'
import { BlogUpdateIn } from 'types/internal/media/input'
import { Blog } from 'types/internal/media/output'
import { Option } from 'types/internal/other'
import { putManageBlog } from 'api/internal/manage/update'
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

const TextEditor = dynamic(() => import('components/widgets/TextEditor'), { ssr: false })

interface Props {
  data: Blog
  channels: Channel[]
}

export default function ManageBlogEdit(props: Props): React.JSX.Element {
  const { data, channels } = props

  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))

  const router = useRouter()
  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const { toast, handleToast } = useToast()
  const { handleError } = useApiError({ handleToast })
  const [values, setValues] = useState<BlogUpdateIn>({ title: data.title, content: data.content, richtext: data.richtext, publish: data.publish })

  const handleBack = () => router.push('/manage/blog')
  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })

  const handleRichtext = (html: string) => {
    const richtext = html.trim() === '<p></p>' ? '' : html.trim()
    setValues({ ...values, richtext })
  }

  const handleForm = async () => {
    const { title, content, richtext } = values
    if (!isRequiredCheck({ title, content, richtext })) return
    handleLoading(true)
    const ret = await putManageBlog(data.ulid, values)
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
    <Main title="ブログ編集" type="table" toast={toast} isFooter={false} button={button}>
      <form method="POST" action="">
        <VStack gap="8">
          <ToggleCard label="公開する" isActive={values.publish} onClick={handlePublish} />
          <SelectBox label="チャンネル" name="channelUlid" value={data.channel.ulid} options={channelOptions} disabled />
          <Input label="タイトル" name="title" value={values.title} required={isRequired} onChange={handleInput} />
          <Textarea label="内容" name="content" value={values.content} required={isRequired} onChange={handleText} />
          <InputFile label="サムネイル" accept="image/*" onChange={handleFile} />
          <TextEditor label="本文" value={values.richtext} required={isRequired} onChange={handleRichtext} />
        </VStack>
      </form>
    </Main>
  )
}
