import { useState, ChangeEvent } from 'react'
import { Channel } from 'types/internal/channel'
import { MusicIn } from 'types/internal/media/input'
import { Option } from 'types/internal/other'
import { postMusicCreate } from 'api/internal/manage/create'
import { FetchError } from 'utils/constants/enum'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import CheckBox from 'components/parts/Input/CheckBox'
import InputFile from 'components/parts/Input/File'
import SelectBox from 'components/parts/Input/SelectBox'
import Textarea from 'components/parts/Input/Textarea'
import ToggleCard from 'components/parts/Input/ToggleCard'
import VStack from 'components/parts/Stack/Vertical'

interface Props {
  channels: Channel[]
}

export default function MusicCreate(props: Props): React.JSX.Element {
  const { channels } = props

  const channelUlid = channels.find((c) => c.isDefault)?.ulid ?? ''
  const channelOptions: Option[] = channels.map((c) => ({ label: c.name, value: c.ulid }))

  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const { toast, handleToast } = useToast()
  const [values, setValues] = useState<MusicIn>({ channelUlid, publish: true, title: '', content: '', lyric: '', download: true })

  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleCheck = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.checked })
  const handleFile = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, music: files })

  const handleForm = async () => {
    const { channelUlid, title, content, music } = values
    if (!isRequiredCheck({ channelUlid, title, content, music })) return
    handleLoading(true)
    const ret = await postMusicCreate(values)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(FetchError.Post, true)
      return
    }
    setValues({ channelUlid, publish: true, title: '', content: '', lyric: '', download: true })
    handleToast('作成しました', false)
  }

  return (
    <Main title="Music" type="table" toast={toast} isFooter={false} button={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <form method="POST" action="" encType="multipart/form-data">
        <VStack gap="8">
          <ToggleCard label="公開する" isActive={values.publish} onClick={handlePublish} />
          <SelectBox label="チャンネル" name="channelUlid" value={values.channelUlid} options={channelOptions} onChange={handleSelect} />
          <Input label="タイトル" name="title" required={isRequired} onChange={handleInput} />
          <Textarea label="内容" name="content" required={isRequired} onChange={handleText} />
          <Textarea label="歌詞" name="lyric" required={isRequired} onChange={handleText} />
          <VStack gap="2">
            <InputFile label="音楽" accept="audio/*" required={isRequired} onChange={handleFile} />
            <CheckBox label="ダウンロード許可" name="download" defaultChecked onChange={handleCheck} />
          </VStack>
        </VStack>
      </form>
    </Main>
  )
}
