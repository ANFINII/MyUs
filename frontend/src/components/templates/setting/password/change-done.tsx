import { useTranslation } from 'react-i18next'
import cx from 'utils/functions/cx'
import { useAppRouter } from 'components/hooks/useAppRouter'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import VStack from 'components/parts/Stack/Vertical'
import style from '../Setting.module.scss'

export default function PasswordChangeDone(): React.JSX.Element {
  const router = useAppRouter()
  const { t } = useTranslation()
  const handleBack = () => router.push('/setting/profile')

  return (
    <Main title={t('setting.password.title')}>
      <article className={style.article_pass}>
        <div className={cx(style.form_account, style.password_done)}>
          <p className="fs_14">{t('setting.password.done')}</p>
          <VStack className="mv_24">
            <Button color="blue" size="l" name={t('status.back')} onClick={handleBack} />
          </VStack>
        </div>
      </article>
      <Footer />
    </Main>
  )
}
