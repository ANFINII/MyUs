import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { WithdrawalIn } from 'types/internal/auth'
import { postWithdrawal } from 'api/internal/auth'
import { FetchError } from 'utils/constants/enum'
import { encrypt } from 'utils/functions/encrypt'
import { useLoading } from 'components/hooks/useLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import { useUser } from 'components/hooks/useUser'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Alert from 'components/parts/Alert'
import Button from 'components/parts/Button'
import Password from 'components/parts/Input/Password'
import VStack from 'components/parts/Stack/Vertical'
import style from '../Account.module.scss'

export default function WithdrawalConfirm(): React.JSX.Element {
  const router = useRouter()
  const { t } = useTranslation()
  const { resetUser } = useUser()
  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const [values, setValues] = useState<WithdrawalIn>({ password: '' })

  const handleBack = () => router.push('/account/withdrawal')
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })

  const handleSubmit = async () => {
    const { password } = values
    if (!validate({ password })) return

    handleLoading(true)
    const request: WithdrawalIn = { password: encrypt(password) }
    const ret = await postWithdrawal(request)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(FetchError.Post, true)
      return
    }
    resetUser()
    router.push('/account/login')
  }

  return (
    <Main metaTitle={t('account.withdrawal.title')} toast={toast}>
      <article className={style.account}>
        <form method="POST" action="" className={style.form}>
          <h1 className={style.title}>{t('account.withdrawal.title')}</h1>
          <VStack gap="8">
            <Alert type="error">{t('account.withdrawal.confirm')}</Alert>
            <Password value={values.password} name="password" placeholder={t('account.form.password')} error={error} onChange={handleInput} />
          </VStack>

          <VStack gap="12" className="mv_40">
            <Button color="red" size="l" name={t('account.withdrawal.submit')} loading={loading} onClick={handleSubmit} />
            <Button color="blue" size="l" name={t('status.back')} onClick={handleBack} />
          </VStack>
        </form>
      </article>
      <Footer />
    </Main>
  )
}
