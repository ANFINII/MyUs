import { useTranslation } from 'react-i18next'
import { useRouter } from 'components/hooks/useRouter'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import style from './Cancel.module.scss'

export default function PaymentCancel(): React.JSX.Element {
  const router = useRouter()
  const { t } = useTranslation()
  const handleBack = () => router.push('/setting/payment')

  return (
    <Main metaTitle={t('setting.payment.checkoutCancelTitle')}>
      <div className={style.cancel}>
        <h1 className={style.title}>{t('setting.payment.checkoutCancelHeading')}</h1>
        <p className={style.message}>{t('setting.payment.checkoutCancelMessage')}</p>
        <Button color="blue" name={t('setting.payment.backToPlans')} onClick={handleBack} />
      </div>
    </Main>
  )
}
