import { useState, ChangeEvent } from 'react'
import { Channel } from 'types/internal/channel'
import { ChatIn } from 'types/internal/media'
import { Option } from 'types/internal/other'
import { postChatCreate } from 'api/internal/media/create'
import { FetchError } from 'utils/constants/enum'
import { nowDate } from 'utils/functions/datetime'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import SelectBox from 'components/parts/Input/SelectBox'
import Textarea from 'components/parts/Input/Textarea'
import ToggleCard from 'components/parts/Input/ToggleCard'
import VStack from 'components/parts/Stack/Vertical'

interface Props {
  channels: Channel[]
}

export default function ChatCreate(props: Props): React.JSX.Element {
  const { channels } = props

  const channelUlid = channels.find((c) => c.isDefault)?.ulid ?? ''
  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))

  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const { toast, handleToast } = useToast()
  const [values, setValues] = useState<ChatIn>({ channelUlid, publish: true, title: '', content: '', period: '' })

  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })

  const handleForm = async () => {
    const { channelUlid, title, content, period } = values
    if (!isRequiredCheck({ channelUlid, title, content, period })) return
    handleLoading(true)
    const ret = await postChatCreate(values)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(FetchError.Post, true)
      return
    }
    setValues({ channelUlid, publish: true, title: '', content: '', period: '' })
    handleToast('作成しました', false)
  }

  return (
    <Main title="Chat" type="table" toast={toast} isFooter={false} button={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <form method="POST" action="">
        <VStack gap="8">
          <ToggleCard label="公開する" isActive={values.publish} onClick={handlePublish} />
          <SelectBox label="チャンネル" name="channelUlid" value={values.channelUlid} options={channelOptions} onChange={handleSelect} />
          <Input label="タイトル" name="title" required={isRequired} onChange={handleInput} />
          <Textarea label="内容" name="content" required={isRequired} onChange={handleText} />
          <Input label="期間" name="period" placeholder={`${nowDate.year}-12-31`} required={isRequired} onChange={handleInput} />
        </VStack>
      </form>
    </Main>
  )
}
