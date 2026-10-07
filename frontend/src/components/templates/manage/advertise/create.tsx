import { useState, ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from '@tanstack/react-router'
import { AdvertiseIn } from 'types/internal/advertise'
import { postAdvertiseCreate } from 'api/internal/manage/create'
import { Fetch, FetchError } from 'utils/constants/enum'
import { useLoading } from 'components/hooks/useLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import DatePicker from 'components/parts/Input/DatePicker'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'
import ToggleCard from 'components/parts/Input/ToggleCard'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'

export default function AdvertiseCreate(): React.JSX.Element {
  const navigate = useNavigate()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const [values, setValues] = useState<AdvertiseIn>({ title: '', url: '', content: '', publish: true, period: null })

  const handleBack = () => navigate({ to: '/manage/advertise' })
  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handlePeriod = (period: string) => setValues({ ...values, period: period || null })
  const handleImage = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })
  const handleVideo = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, video: files })

  const handleForm = async () => {
    const { title, url, content, image } = values
    if (!validate({ title, url, content, image })) return
    handleLoading(true)
    const ret = await postAdvertiseCreate(values)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(FetchError.Post, true)
      return
    }
    setValues({ title: '', url: '', content: '', publish: true, period: null })
    handleToast(Fetch.Create, false)
  }

  const button = (
    <HStack gap="4">
      <Button color="green" size="s" name={t('manage.button.create')} loading={loading} onClick={handleForm} />
      <Button color="blue" size="s" name={t('status.back')} onClick={handleBack} />
    </HStack>
  )

  return (
    <Main title="Advertise" type="table" toast={toast} isFooter={false} button={button}>
      <form method="POST" action="" encType="multipart/form-data">
        <VStack gap="8">
          <ToggleCard label={t('manage.form.publish')} isActive={values.publish} onClick={handlePublish} />
          <Input label={t('manage.form.title')} name="title" required error={error} onChange={handleInput} />
          <Input label={t('manage.form.url')} name="url" type="url" required error={error} onChange={handleInput} />
          <Textarea label={t('manage.form.content')} name="content" required error={error} onChange={handleText} />
          <InputFile label={t('manage.form.image')} accept="image/*" required error={error} onChange={handleImage} />
          <InputFile label={t('manage.form.video')} accept="video/*" onChange={handleVideo} />
          <DatePicker label={t('manage.form.period')} name="period" value={values.period ?? ''} onChange={handlePeriod} />
        </VStack>
      </form>
    </Main>
  )
}
