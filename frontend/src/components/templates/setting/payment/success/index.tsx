import { useTranslation } from 'react-i18next'
import { useAppRouter } from 'components/hooks/useAppRouter'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import style from './Success.module.scss'

export default function PaymentSuccess(): React.JSX.Element {
  const router = useAppRouter()
  const { t } = useTranslation()
  const handleBack = () => router.push('/setting/payment')

  return (
    <Main metaTitle={t('setting.payment.successTitle')}>
      <div className={style.success}>
        <h1 className={style.title}>{t('setting.payment.successHeading')}</h1>
        <p className={style.message}>
          {t('setting.payment.thanks')}
          <br />
          {t('setting.payment.reflect')}
        </p>
        <Button color="blue" name={t('setting.payment.backToPlans')} onClick={handleBack} />
      </div>
    </Main>
  )
}
