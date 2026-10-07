import { useTranslation } from 'react-i18next'
import { useNavigate } from '@tanstack/react-router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Alert from 'components/parts/Alert'
import Button from 'components/parts/Button'
import VStack from 'components/parts/Stack/Vertical'
import style from '../Account.module.scss'

export default function Withdrawal(): React.JSX.Element {
  const navigate = useNavigate()
  const { t } = useTranslation()
  const handleBack = () => navigate({ to: '/' })
  const handleNext = () => navigate({ to: '/account/withdrawal/confirm' })

  return (
    <Main metaTitle={t('account.withdrawal.title')}>
      <article className={style.account}>
        <div className={style.form}>
          <h1 className={style.title}>{t('account.withdrawal.title')}</h1>
          <VStack gap="8">
            <Alert type="error">
              {t('account.withdrawal.warning')}
              <br />
              {t('account.withdrawal.irreversible')}
            </Alert>
          </VStack>

          <VStack gap="12" className="mv_40">
            <Button color="red" size="l" name={t('account.withdrawal.next')} onClick={handleNext} />
            <Button color="blue" size="l" name={t('sideMenu.home')} onClick={handleBack} />
          </VStack>
        </div>
      </article>
      <Footer />
    </Main>
  )
}
