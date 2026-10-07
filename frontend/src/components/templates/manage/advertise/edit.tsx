import { useState, ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from '@tanstack/react-router'
import { Advertise, AdvertiseUpdateIn } from 'types/internal/advertise'
import { putManageAdvertise } from 'api/internal/manage/update'
import { Fetch, FetchError } from 'utils/constants/enum'
import { useApiError } from 'components/hooks/useApiError'
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

interface Props {
  data: Advertise
}

export default function ManageAdvertiseEdit(props: Props): React.JSX.Element {
  const { data } = props

  const navigate = useNavigate()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const { handleError } = useApiError({ handleToast })
  const [values, setValues] = useState<AdvertiseUpdateIn>({ title: data.title, url: data.url, content: data.content, publish: data.publish, period: data.period })

  const handleBack = () => navigate({ to: '/manage/advertise' })
  const handlePublish = () => setValues({ ...values, publish: !values.publish })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handlePeriod = (period: string) => setValues({ ...values, period: period || null })
  const handleImage = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, image: files })
  const handleVideo = (files: File | File[]) => Array.isArray(files) || setValues({ ...values, video: files })

  const handleForm = async () => {
    const { title, url, content } = values
    if (!validate({ title, url, content })) return
    handleLoading(true)
    const ret = await putManageAdvertise(data.ulid, values)
    handleLoading(false)
    if (ret.isErr()) {
      handleError(FetchError.Put, ret.error.message)
      return
    }
    handleToast(Fetch.Save, false)
  }

  const button = (
    <HStack gap="4">
      <Button color="green" size="s" name={t('manage.button.save')} loading={loading} onClick={handleForm} />
      <Button color="blue" size="s" name={t('status.back')} onClick={handleBack} />
    </HStack>
  )

  return (
    <Main title="Advertise" type="table" toast={toast} isFooter={false} button={button}>
      <form method="POST" action="" encType="multipart/form-data">
        <VStack gap="8">
          <ToggleCard label={t('manage.form.publish')} isActive={values.publish} onClick={handlePublish} />
          <Input label={t('manage.form.title')} name="title" value={values.title} required error={error} onChange={handleInput} />
          <Input label={t('manage.form.url')} name="url" type="url" value={values.url} required error={error} onChange={handleInput} />
          <Textarea label={t('manage.form.content')} name="content" value={values.content} required error={error} onChange={handleText} />
          <InputFile label={t('manage.form.image')} accept="image/*" required error={error} onChange={handleImage} />
          <InputFile label={t('manage.form.video')} accept="video/*" onChange={handleVideo} />
          <DatePicker label={t('manage.form.displayPeriod')} name="period" value={values.period ?? ''} onChange={handlePeriod} />
        </VStack>
      </form>
    </Main>
  )
}
