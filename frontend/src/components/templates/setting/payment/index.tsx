import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { MypageOut } from 'types/internal/user'
import { postPaymentCancel, postPaymentCheckout } from 'api/internal/payment'
import { FetchError } from 'utils/constants/enum'
import { useAppRouter } from 'components/hooks/useAppRouter'
import { useLoading } from 'components/hooks/useLoading'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Modal from 'components/parts/Modal'
import CurrentBanner from './CurrentBanner'
import style from './Payment.module.scss'
import PlanCard from './PlanCard'
import { plans } from './plans'

interface Props {
  mypage: MypageOut
}

export default function Payment(props: Props): React.JSX.Element {
  const { mypage } = props

  const router = useAppRouter()
  const { t, i18n } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { toast, handleToast } = useToast()
  const [isModal, setIsModal] = useState<boolean>(false)
  const [selectedPlan, setSelectedPlan] = useState<string>('')

  const currentPlan = mypage.plan
  const purchasable = plans.filter((plan) => plan.name !== 'Free')
  const isPaid = currentPlan !== 'Free'

  const handleChange = () => router.push('/setting/payment/change')

  const handlePurchase = async (plan: string) => {
    setSelectedPlan(plan)
    const ret = await postPaymentCheckout({ plan })
    if (ret.isErr()) {
      setSelectedPlan('')
      handleToast(ret.error.message ?? FetchError.Post, true)
      return
    }
    window.location.href = ret.value.url
  }

  const handleModal = () => setIsModal(!isModal)

  const handleCancelSubmit = async () => {
    handleLoading(true)
    const ret = await postPaymentCancel()
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(ret.error.message ?? FetchError.Post, true)
      return
    }
    setIsModal(false)
    const periodEnd = new Date(ret.value.periodEnd).toLocaleDateString(i18n.language)
    handleToast(t('setting.payment.cancelReserved', { periodEnd }), false)
    router.reload()
  }

  return (
    <Main metaTitle={t('setting.payment.title')} toast={toast}>
      <div className={style.payment}>
        <CurrentBanner planName={currentPlan} />

        <div className={style.plans}>
          {purchasable.map((plan) => (
            <PlanCard key={plan.name} plan={plan} active={currentPlan === plan.name} disabled={isPaid} loading={selectedPlan === plan.name} onPurchase={handlePurchase} />
          ))}
        </div>

        {isPaid && (
          <div className={style.actions}>
            <Button color="green" name={t('setting.payment.change')} onClick={handleChange} />
            <Button color="red" name={t('setting.payment.cancel')} onClick={handleModal} />
          </div>
        )}
      </div>

      <Modal
        open={isModal}
        onClose={handleModal}
        title={t('setting.payment.cancelTitle')}
        actions={[
          { name: t('setting.button.cancel'), color: 'white', onClick: handleModal, disabled: loading },
          { name: t('setting.payment.cancel'), color: 'red', onClick: handleCancelSubmit, loading },
        ]}
      >
        <p>{t('setting.payment.cancelConfirm')}</p>
        <p>{t('setting.payment.cancelNotice')}</p>
      </Modal>
    </Main>
  )
}
