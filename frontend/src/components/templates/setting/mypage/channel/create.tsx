import { ChangeEvent, useState } from 'react'
import { useRouter } from 'next/router'
import { ChannelIn } from 'types/internal/channel'
import { postChannel } from 'api/internal/channel'
import { FetchError } from 'utils/constants/enum'
import { useApiError } from 'components/hooks/useApiError'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import ExImage from 'components/parts/ExImage'
import IconPerson from 'components/parts/Icon/Person'
import Input from 'components/parts/Input'
import InputImage from 'components/parts/Input/Image'
import Textarea from 'components/parts/Input/Textarea'
import VStack from 'components/parts/Stack/Vertical'
import style from '../../Setting.module.scss'

const initChannel: ChannelIn = {
  name: '',
  description: '',
}

export default function ChannelCreate(): React.JSX.Element {
  const router = useRouter()
  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const { toast, handleToast } = useToast()
  const { message, handleError } = useApiError({ handleToast })
  const [avatarFile, setAvatarFile] = useState<File>()
  const [values, setValues] = useState<ChannelIn>(initChannel)

  const avatarUrl = avatarFile ? URL.createObjectURL(avatarFile) : ''

  const handleBack = () => router.push('/setting/mypage')
  const handleAvatar = (files: File | File[]) => Array.isArray(files) || setAvatarFile(files)
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleText = (e: ChangeEvent<HTMLTextAreaElement>) => setValues({ ...values, [e.target.name]: e.target.value })

  const handleSubmit = async () => {
    const { name } = values
    if (!isRequiredCheck({ name })) return
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
    <Main metaTitle="チャンネル作成" toast={toast}>
      <article className="article_registration">
        <form method="POST" action="" className="form_account">
          <h1 className="signup_h1">チャンネル作成</h1>

          {message && (
            <ul className="messages_signup">
              <li>{message}</li>
            </ul>
          )}

          <VStack gap="8">
            <VStack gap="4" align="center">
              <p>アバター画像</p>
              <InputImage
                id="avatar"
                className={style.account_image_edit}
                icon={
                  avatarUrl ? (
                    <div className={style.account_image}>
                      <ExImage src={avatarUrl} size="56" />
                    </div>
                  ) : (
                    <div className={style.account_image_edit}>
                      <IconPerson size="56" type="square" />
                    </div>
                  )
                }
                onChange={handleAvatar}
              />
            </VStack>

            <Input name="name" placeholder="チャンネル名" maxLength={50} required={isRequired} onChange={handleInput} />
            <Textarea name="description" placeholder="説明" onChange={handleText} />
          </VStack>

          <VStack gap="12" className="mv_40">
            <Button color="green" size="l" name="作成" type="submit" loading={isLoading} onClick={handleSubmit} />
            <Button color="blue" size="l" name="戻る" onClick={handleBack} />
          </VStack>
        </form>
      </article>
      <Footer />
    </Main>
  )
}
