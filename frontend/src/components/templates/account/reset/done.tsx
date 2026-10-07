import { useTranslation } from 'react-i18next'
import { useAppRouter } from 'components/hooks/useAppRouter'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import VStack from 'components/parts/Stack/Vertical'
import style from '../Account.module.scss'

export default function ResetDone(): React.JSX.Element {
  const router = useAppRouter()
  const { t } = useTranslation()
  const handleBack = () => router.push('/account/login')

  return (
    <Main metaTitle={t('account.reset.confirmTitle')}>
      <article className={style.account}>
        <div className={style.form}>
          <h1 className={style.title}>{t('account.reset.confirmTitle')}</h1>
          <p className="fs_14">{t('account.reset.done')}</p>
          <VStack gap="12" className="mv_40">
            <Button color="blue" size="l" name={t('status.login')} onClick={handleBack} />
          </VStack>
        </div>
      </article>
      <Footer />
    </Main>
  )
}
