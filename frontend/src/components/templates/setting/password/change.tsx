import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { PasswordChangeIn } from 'types/internal/auth'
import { postPasswordChange } from 'api/internal/auth'
import { FetchError } from 'utils/constants/enum'
import { encrypt } from 'utils/functions/encrypt'
import { useLoading } from 'components/hooks/useLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Password from 'components/parts/Input/Password'
import VStack from 'components/parts/Stack/Vertical'
import style from '../Setting.module.scss'

export default function PasswordChange(): React.JSX.Element {
  const router = useRouter()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const [values, setValues] = useState<PasswordChangeIn>({ oldPassword: '', password1: '', password2: '' })

  const handleBack = () => router.push('/setting/profile')
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })

  const handleSubmit = async () => {
    const { oldPassword, password1, password2 } = values
    if (!validate({ oldPassword, password1, password2 })) return
    if (password1 !== password2) {
      handleToast(t('setting.password.mismatch'), true)
      return
    }
    handleLoading(true)
    const request: PasswordChangeIn = {
      oldPassword: encrypt(oldPassword),
      password1: encrypt(password1),
      password2: encrypt(password2),
    }
    const ret = await postPasswordChange(request)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(FetchError.Post, true)
      return
    }
    router.push('/setting/password/change-done')
  }

  return (
    <Main title={t('setting.password.title')} toast={toast}>
      <article className={style.article_pass}>
        <form method="POST" action="" className={style.form_account}>
          <VStack gap="8">
            <Password value={values.oldPassword} name="oldPassword" placeholder={t('setting.password.old')} error={error} onChange={handleInput} />
            <Password value={values.password1} name="password1" placeholder={t('setting.password.new')} error={error} onChange={handleInput} />
            <Password value={values.password2} name="password2" placeholder={t('setting.password.confirm')} error={error} onChange={handleInput} />
          </VStack>

          <VStack gap="12" className="mv_40">
            <Button color="green" size="l" name={t('setting.button.change')} loading={loading} onClick={handleSubmit} />
            <Button color="blue" size="l" name={t('status.back')} onClick={handleBack} />
          </VStack>
        </form>
      </article>
      <Footer />
    </Main>
  )
}
