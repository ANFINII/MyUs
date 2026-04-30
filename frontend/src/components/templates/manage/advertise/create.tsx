import { useState, ChangeEvent } from 'react'
import { AdvertiseIn } from 'types/internal/advertise'
import { postAdvertiseCreate } from 'api/internal/manage/create'
import { FetchError } from 'utils/constants/enum'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'
import ToggleCard from 'components/parts/Input/ToggleCard'
import VStack from 'components/parts/Stack/Vertical'

export default function AdvertiseCreate(): React.JSX.Element {
  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const { toast, handleToast } = useToast()
  const [values, setValues] = useState<AdvertiseIn>({ title: '', url: '', content: '', publish: true, period: null })

  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handlePeriod = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, period: e.target.value || null })
  const handleImage = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })
  const handleVideo = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, video: files })

  const handleForm = async () => {
    const { title, url, content, image } = values
    if (!isRequiredCheck({ title, url, content, image })) return
    handleLoading(true)
    const ret = await postAdvertiseCreate(values)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(FetchError.Post, true)
      return
    }
    setValues({ title: '', url: '', content: '', publish: true, period: null })
    handleToast('作成しました', false)
  }

  return (
    <Main title="広告作成" type="table" toast={toast} isFooter={false} button={<Button color="green" size="s" name="作成する" loading={isLoading} onClick={handleForm} />}>
      <form method="POST" action="" encType="multipart/form-data">
        <VStack gap="8">
          <ToggleCard label="公開する" isActive={values.publish} onClick={handlePublish} />
          <Input label="タイトル" name="title" required={isRequired} onChange={handleInput} />
          <Input label="リンク URL" name="url" type="url" required={isRequired} onChange={handleInput} />
          <Textarea label="内容" name="content" required={isRequired} onChange={handleText} />
          <Input label="表示期限" name="period" type="date" onChange={handlePeriod} />
          <InputFile label="画像（必須）" accept="image/*" required={isRequired} onChange={handleImage} />
          <InputFile label="動画（任意）" accept="video/*" onChange={handleVideo} />
        </VStack>
      </form>
    </Main>
  )
}
