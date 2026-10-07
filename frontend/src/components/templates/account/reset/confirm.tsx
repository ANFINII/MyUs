import { ChangeEvent, useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useSearch } from '@tanstack/react-router'
import { PasswordResetIn } from 'types/internal/auth'
import { getPasswordResetVerify, postPasswordReset } from 'api/internal/auth'
import { FetchError } from 'utils/constants/enum'
import { encrypt } from 'utils/functions/encrypt'
import { useAppRouter } from 'components/hooks/useAppRouter'
import { useLoading } from 'components/hooks/useLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Password from 'components/parts/Input/Password'
import VStack from 'components/parts/Stack/Vertical'
import style from '../Account.module.scss'

export default function ResetConfirm(): React.JSX.Element {
  const router = useAppRouter()
  const { t } = useTranslation()
  const { token } = useSearch({ strict: false })
  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const [email, setEmail] = useState<string>('')
  const [isVerified, setIsVerified] = useState<boolean>(false)
  const [values, setValues] = useState<PasswordResetIn>({ token: '', password1: '', password2: '' })

  const handleBack = () => router.push('/account/login')
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })

  useEffect(() => {
    if (!token) {
      router.push('/account/login')
      return
    }
    const verify = async () => {
      const ret = await getPasswordResetVerify(token)
      if (ret.isErr()) {
        router.push('/account/login')
        return
      }
      setValues((prev) => ({ ...prev, token }))
      setEmail(ret.value.email)
      setIsVerified(true)
    }
    verify()
  }, [router, token])

  const handleSubmit = async () => {
    const { password1, password2 } = values
    if (!validate({ password1, password2 })) return
    if (password1 !== password2) {
      handleToast(t('account.form.passwordMismatch'), true)
      return
    }
    handleLoading(true)
    const request: PasswordResetIn = {
      token: values.token,
      password1: encrypt(password1),
      password2: encrypt(password2),
    }
    const ret = await postPasswordReset(request)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(ret.error.message ?? FetchError.Post, true)
      return
    }
    router.push('/account/reset/done')
  }

  return (
    <Main metaTitle={t('account.reset.confirmTitle')} toast={toast}>
      <article className={style.account}>
        <form method="POST" action="" className={style.form}>
          <h1 className={style.title}>{t('account.reset.confirmTitle')}</h1>
          {isVerified && (
            <>
              <VStack gap="8">
                <Input type="email" name="email" value={email} disabled maxLength={255} />
                <Password value={values.password1} name="password1" placeholder={t('account.form.passwordNew')} error={error} onChange={handleInput} />
                <Password value={values.password2} name="password2" placeholder={t('account.form.passwordConfirm')} error={error} onChange={handleInput} />
              </VStack>

              <VStack gap="12" className="mv_40">
                <Button color="green" size="l" name={t('account.reset.submit')} type="submit" loading={loading} onClick={handleSubmit} />
                <Button color="blue" size="l" name={t('status.back')} onClick={handleBack} />
              </VStack>
            </>
          )}
        </form>
      </article>
      <Footer />
    </Main>
  )
}
