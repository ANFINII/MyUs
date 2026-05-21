import { useState } from 'react'
import { useRouter } from 'next/router'
import { MypageOut } from 'types/internal/user'
import { postPaymentCancel, postPaymentCheckout } from 'api/internal/payment'
import { FetchError } from 'utils/constants/enum'
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
  const router = useRouter()
  const { toast, handleToast } = useToast()
  const [loadingPlan, setLoadingPlan] = useState<string>('')
  const [isCancelOpen, setIsCancelOpen] = useState<boolean>(false)
  const [isCancelLoading, setIsCancelLoading] = useState<boolean>(false)

  const currentPlan = mypage.plan
  const purchasable = plans.filter((plan) => plan.name !== 'Free')
  const isPaid = currentPlan !== 'Free'

  const handleChange = () => router.push('/setting/payment/change')

  const handlePurchase = async (plan: string) => {
    setLoadingPlan(plan)
    const ret = await postPaymentCheckout({ plan })
    if (ret.isErr()) {
      setLoadingPlan('')
      handleToast(ret.error.message ?? FetchError.Post, true)
      return
    }
    window.location.href = ret.value.url
  }

  const handleCancelOpen = () => setIsCancelOpen(true)
  const handleCancelClose = () => setIsCancelOpen(false)

  const handleCancelSubmit = async () => {
    setIsCancelLoading(true)
    const ret = await postPaymentCancel()
    setIsCancelLoading(false)
    if (ret.isErr()) {
      handleToast(ret.error.message ?? FetchError.Post, true)
      return
    }
    setIsCancelOpen(false)
    const periodEnd = new Date(ret.value.periodEnd).toLocaleDateString('ja-JP')
    handleToast(`解約予約完了。${periodEnd} まで利用可能です`, false)
    router.reload()
  }

  return (
    <Main metaTitle="料金プラン" toast={toast}>
      <div className={style.payment}>
        <CurrentBanner planName={currentPlan} />

        <div className={style.plans}>
          {purchasable.map((plan) => (
            <PlanCard key={plan.name} plan={plan} active={currentPlan === plan.name} purchaseDisabled={isPaid} loading={loadingPlan === plan.name} onPurchase={handlePurchase} />
          ))}
        </div>

        {isPaid && (
          <div className={style.actions}>
            <Button color="green" name="プランを変更" onClick={handleChange} />
            <Button color="red" name="解約する" onClick={handleCancelOpen} />
          </div>
        )}
      </div>

      <Modal
        open={isCancelOpen}
        onClose={handleCancelClose}
        title="解約の確認"
        actions={[
          { name: 'キャンセル', color: 'white', onClick: handleCancelClose, disabled: isCancelLoading },
          { name: '解約する', color: 'red', onClick: handleCancelSubmit, loading: isCancelLoading },
        ]}
      >
        <p>本当に解約しますか？</p>
        <p>解約後は次回更新日まで現在のプランをご利用いただけます。</p>
      </Modal>
    </Main>
  )
}
