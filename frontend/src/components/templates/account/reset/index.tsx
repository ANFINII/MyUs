import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from '@tanstack/react-router'
import { postPasswordResetEmail } from 'api/internal/auth'
import { FetchError } from 'utils/constants/enum'
import { useLoading } from 'components/hooks/useLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Alert from 'components/parts/Alert'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import VStack from 'components/parts/Stack/Vertical'
import style from '../Account.module.scss'

export default function Reset(): React.JSX.Element {
  const navigate = useNavigate()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const [email, setEmail] = useState<string>('')

  const handleBack = () => navigate({ to: '/account/login' })
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)

  const handleSubmit = async () => {
    if (!validate({ email })) return
    handleLoading(true)
    const ret = await postPasswordResetEmail(email)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(ret.error.message ?? FetchError.Error, true)
      return
    }
    handleToast(t('account.form.mailSent'), false)
  }

  return (
    <Main metaTitle={t('account.reset.title')} toast={toast}>
      <article className={style.account}>
        <form method="POST" action="" className={style.form}>
          <h1 className={style.title}>{t('account.reset.title')}</h1>
          <VStack gap="8">
            <Input type="email" name="email" placeholder={t('account.form.email')} maxLength={255} required error={error} onChange={handleInput} />
            <Alert type="info">{t('account.reset.emailNotice')}</Alert>
          </VStack>

          <VStack gap="12" className="mv_40">
            <Button color="green" size="l" name={t('account.form.send')} type="submit" loading={loading} onClick={handleSubmit} />
            <Button color="blue" size="l" name={t('status.back')} onClick={handleBack} />
          </VStack>
        </form>
      </article>
      <Footer />
    </Main>
  )
}
