import { ChangeEvent, FormEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { PasswordResetIn } from 'types/internal/auth'
import { postPasswordReset } from 'api/internal/auth'
import { FetchError } from 'utils/constants/enum'
import { useApiError } from 'components/hooks/useApiError'
import { useLoading } from 'components/hooks/useLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Alert from 'components/parts/Alert'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Password from 'components/parts/Input/Password'
import VStack from 'components/parts/Stack/Vertical'
import style from '../../Account.module.scss'

interface Props {
  token: string
  email: string
}

export default function ResetConfirm(props: Props): React.JSX.Element {
  const { token, email } = props

  const router = useRouter()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const { message, setMessage, handleError } = useApiError({ handleToast })
  const [values, setValues] = useState<PasswordResetIn>({ token, password1: '', password2: '' })

  const handleBack = () => router.push('/account/login')
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (loading) return
    const { password1, password2 } = values
    if (!validate({ password1, password2 })) return
    if (password1 !== password2) {
      setMessage(t('account.form.passwordMismatch'))
      return
    }
    handleLoading(true)
    const request: PasswordResetIn = { token: values.token, password1, password2 }
    const ret = await postPasswordReset(request)
    handleLoading(false)
    if (ret.isErr()) {
      handleError(FetchError.Post, ret.error.message)
      return
    }
    router.push('/account/reset/done')
  }

  return (
    <Main metaTitle={t('account.reset.confirmTitle')} size="s" toast={toast} isFooter>
      <article className={style.account}>
        <form method="POST" action="" className={style.form} onSubmit={handleSubmit}>
          <h1 className={style.title}>{t('account.reset.confirmTitle')}</h1>
          <div className={style.message}>
            {message && (
              <Alert type="error" isPlain className={style.error}>{message}</Alert>
            )}
          </div>
          <VStack gap="8">
            <Input type="email" name="email" value={email} disabled maxLength={255} />
            <Password value={values.password1} name="password1" placeholder={t('account.form.passwordNew')} error={error} onChange={handleInput} />
            <Password value={values.password2} name="password2" placeholder={t('account.form.passwordConfirm')} error={error} onChange={handleInput} />
          </VStack>

          <VStack gap="12" className="mv_40">
            <Button color="green" size="l" name={t('account.reset.submit')} type="submit" loading={loading} />
            <Button color="blue" size="l" name={t('status.back')} onClick={handleBack} />
          </VStack>
        </form>
      </article>
    </Main>
  )
}
