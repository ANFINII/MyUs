import { useState, ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { Advertise, AdvertiseUpdateIn } from 'types/internal/advertise'
import { putManageAdvertise } from 'api/internal/manage/update'
import { FetchError } from 'utils/constants/enum'
import { useApiError } from 'components/hooks/useApiError'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'
import ToggleCard from 'components/parts/Input/ToggleCard'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'

interface Props {
  data: Advertise
}

export default function ManageAdvertiseEdit(props: Props): React.JSX.Element {
  const { data } = props

  const router = useRouter()
  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const { toast, handleToast } = useToast()
  const { handleError } = useApiError({ handleToast })
  const [values, setValues] = useState<AdvertiseUpdateIn>({
    title: data.title,
    url: data.url,
    content: data.content,
    publish: data.publish,
    period: data.period,
  })

  const handleBack = () => router.push('/manage/advertise')
  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handlePeriod = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, period: e.target.value || null })
  const handleImage = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })
  const handleVideo = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, video: files })

  const handleForm = async () => {
    const { title, url, content } = values
    if (!isRequiredCheck({ title, url, content })) return
    handleLoading(true)
    const ret = await putManageAdvertise(data.ulid, values)
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
    <Main title="広告編集" type="table" toast={toast} isFooter={false} button={button}>
      <form method="POST" action="" encType="multipart/form-data">
        <VStack gap="8">
          <ToggleCard label="公開する" isActive={values.publish} onClick={handlePublish} />
          <Input label="タイトル" name="title" value={values.title} required={isRequired} onChange={handleInput} />
          <Input label="リンク URL" name="url" type="url" value={values.url} required={isRequired} onChange={handleInput} />
          <Textarea label="内容" name="content" value={values.content} required={isRequired} onChange={handleText} />
          <Input label="表示期限" name="period" type="date" value={values.period ?? ''} onChange={handlePeriod} />
          <InputFile label="画像" accept="image/*" onChange={handleImage} />
          <InputFile label="動画" accept="video/*" onChange={handleVideo} />
        </VStack>
      </form>
    </Main>
  )
}
