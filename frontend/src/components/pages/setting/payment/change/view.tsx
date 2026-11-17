import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQueryClient } from '@tanstack/react-query'
import { errorMessage } from 'lib/error'
import { queryKeys } from 'lib/query/keys'
import { PaymentPlanOut } from 'types/internal/payment'
import { MypageOut } from 'types/internal/user'
import { postPaymentCancel, postPaymentChange } from 'api/internal/payment'
import { FetchError } from 'utils/constants/enum'
import { useLoading } from 'components/hooks/useLoading'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Modal from 'components/parts/Modal'
import style from './Change.module.scss'
import CurrentBanner from '../CurrentBanner'
import PlanCard from '../PlanCard'
import { plans } from '../plans'

interface Props {
  mypage: MypageOut
  planPrices: PaymentPlanOut[]
}

export default function PaymentChange(props: Props): React.JSX.Element {
  const { mypage, planPrices } = props

  const router = useRouter()
  const queryClient = useQueryClient()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { toast, handleToast } = useToast()
  const [isModal, setIsModal] = useState<boolean>(false)
  const [isCancelLoading, setIsCancelLoading] = useState<boolean>(false)
  const [activeName, setActiveName] = useState<string>('')

  const currentPlanName = mypage.plan
  const changeable = plans.filter((plan) => plan.name !== 'Free')
  const isChanged = activeName !== '' && activeName !== currentPlanName
  const priceMap = new Map(planPrices.map((p) => [p.name, p.price]))

  const handleBack = () => router.push('/setting/payment')

  const handleSubmit = async () => {
    handleLoading(true)
    const ret = await postPaymentChange({ plan: activeName })
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(errorMessage(ret.error, FetchError.Post), true)
      return
    }
    setActiveName('')
    handleToast(t('setting.payment.changed'), false)
    await queryClient.invalidateQueries({ queryKey: queryKeys.settingMypage })
  }

  const handleModal = () => setIsModal(!isModal)

  const handleCancelSubmit = async () => {
    setIsCancelLoading(true)
    const ret = await postPaymentCancel()
    setIsCancelLoading(false)
    if (ret.isErr()) {
      handleToast(errorMessage(ret.error, FetchError.Post), true)
      return
    }
    setIsModal(false)
    await queryClient.invalidateQueries({ queryKey: queryKeys.settingMypage })
    await queryClient.invalidateQueries({ queryKey: queryKeys.paymentSubscription })
    router.push('/setting/payment')
  }

  return (
    <Main metaTitle={t('setting.payment.changeTitle')} toast={toast}>
      <div className={style.change}>
        <CurrentBanner planName={currentPlanName} notice="" />

        <div className={style.plans}>
          {changeable.map((plan) => (
            <PlanCard
              key={plan.name}
              plan={plan}
              price={priceMap.get(plan.name)}
              active={activeName === plan.name}
              onClick={() => setActiveName(plan.name)}
              current={plan.name === currentPlanName}
              showPurchase={false}
            />
          ))}
        </div>

        <p className={style.currency}>{t('setting.payment.currencyBySubscription')}</p>

        <div className={style.actions}>
          <Button color="green" name={t('setting.button.change')} disabled={!isChanged} loading={loading} onClick={handleSubmit} />
          <Button color="blue" name={t('setting.button.cancel')} onClick={handleBack} />
          <Button color="red" name={t('setting.payment.cancel')} onClick={handleModal} />
        </div>
      </div>

      <Modal
        open={isModal}
        onClose={handleModal}
        title={t('setting.payment.cancelTitle')}
        actions={[
          { name: t('setting.button.cancel'), color: 'white', onClick: handleModal, disabled: isCancelLoading },
          { name: t('setting.payment.cancel'), color: 'red', onClick: handleCancelSubmit, loading: isCancelLoading },
        ]}
      >
        <p>{t('setting.payment.cancelConfirm')}</p>
        <p>{t('setting.payment.cancelNotice')}</p>
      </Modal>
    </Main>
  )
}
