import { useState, ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { Category } from 'types/internal/category'
import { Channel } from 'types/internal/channel'
import { ChatUpdateIn } from 'types/internal/media/input'
import { Chat } from 'types/internal/media/output'
import { Option } from 'types/internal/other'
import { putManageChat } from 'api/internal/manage/update'
import { FetchError } from 'utils/constants/enum'
import { formatDate } from 'utils/functions/datetime'
import { useApiError } from 'components/hooks/useApiError'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import SelectBox from 'components/parts/Input/SelectBox'
import Textarea from 'components/parts/Input/Textarea'
import ToggleCard from 'components/parts/Input/ToggleCard'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'

interface Props {
  data: Chat
  channels: Channel[]
  categories: Category[]
}

export default function ManageChatEdit(props: Props): React.JSX.Element {
  const { data, channels, categories } = props

  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))
  const categoryOptions: Option[] = [{ label: '未選択', value: '' }, ...categories.map((c) => ({ label: c.jpName, value: c.ulid }))]

  const router = useRouter()
  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const { toast, handleToast } = useToast()
  const { handleError } = useApiError({ handleToast })
  const [values, setValues] = useState<ChatUpdateIn>({ categoryUlid: data.categoryUlid, title: data.title, content: data.content, period: formatDate(data.period), publish: data.publish })

  const handleBack = () => router.push('/manage/chat')
  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })

  const handleForm = async () => {
    const { categoryUlid, title, content, period } = values
    if (!isRequiredCheck({ categoryUlid, title, content, period })) return
    handleLoading(true)
    const ret = await putManageChat(data.ulid, values)
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
    <Main title="チャット編集" type="table" toast={toast} isFooter={false} button={button}>
      <form method="POST" action="">
        <VStack gap="8">
          <ToggleCard label="公開する" isActive={values.publish} onClick={handlePublish} />
          <SelectBox label="チャンネル" name="channelUlid" value={data.channel.ulid} options={channelOptions} disabled />
          <SelectBox label="カテゴリー" name="categoryUlid" value={values.categoryUlid} options={categoryOptions} required={isRequired} onChange={handleSelect} />
          <Input label="タイトル" name="title" value={values.title} required={isRequired} onChange={handleInput} />
          <Textarea label="内容" name="content" value={values.content} required={isRequired} onChange={handleText} />
          <Input label="期間" name="period" value={values.period} required={isRequired} onChange={handleInput} />
        </VStack>
      </form>
    </Main>
  )
}
