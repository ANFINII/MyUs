import { ChangeEvent, FormEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { ChannelIn } from 'types/internal/channel'
import { postChannel } from 'api/internal/channel'
import { FetchError } from 'utils/constants/enum'
import { previewUrl } from 'utils/functions/file'
import { useApiError } from 'components/hooks/useApiError'
import { useLoading } from 'components/hooks/useLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Alert from 'components/parts/Alert'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
import VStack from 'components/parts/Stack/Vertical'
import AvatarInput from 'components/widgets/AvatarInput'
import style from '../../../Setting.module.scss'

const initChannel: ChannelIn = {
  name: '',
  description: '',
}

export default function ChannelCreate(): React.JSX.Element {
  const router = useRouter()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const { message, handleError } = useApiError({ handleToast })
  const [avatarFile, setAvatarFile] = useState<File>()
  const [avatarPreview, setAvatarPreview] = useState<string>()
  const [values, setValues] = useState<ChannelIn>(initChannel)

  const avatarUrl = avatarPreview ?? ''

  const handleBack = () => router.push('/setting/mypage')

  const handleAvatar = (file: File) => {
    setAvatarFile(file)
    setAvatarPreview(previewUrl(file, avatarPreview))
  }

  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (loading) return
    const { name } = values
    if (!validate({ name })) return
    handleLoading(true)
    const ret = await postChannel({ ...values, avatarFile })
    handleLoading(false)
    if (ret.isErr()) {
      const message = ret.error.message
      handleError(FetchError.Post, message)
      return
    }
    handleBack()
  }

  return (
    <Main metaTitle={t('setting.channelCreate.title')} size="s" toast={toast} isFooter>
      <article className={style.account}>
        <form method="POST" action="" className={style.form} onSubmit={handleSubmit}>
          <h1 className={style.signup_title}>{t('setting.channelCreate.title')}</h1>
          <div className={style.message}>
            {message && (
              <Alert type="error" isPlain className={style.error}>{message}</Alert>
            )}
          </div>

          <VStack gap="8">
            <VStack gap="4" align="center">
              <p>{t('setting.channelCreate.avatar')}</p>
              <AvatarInput src={avatarUrl} onChange={handleAvatar} />
            </VStack>

            <Input name="name" placeholder={t('setting.channelCreate.name')} maxLength={50} required error={error} onChange={handleInput} />
            <Textarea name="description" placeholder={t('setting.channelCreate.description')} onChange={handleText} />
          </VStack>

          <VStack gap="12" className="mv_40">
            <Button color="green" size="l" name={t('setting.channelCreate.submit')} type="submit" loading={loading} />
            <Button color="blue" size="l" name={t('status.back')} onClick={handleBack} />
          </VStack>
        </form>
      </article>
    </Main>
  )
}
