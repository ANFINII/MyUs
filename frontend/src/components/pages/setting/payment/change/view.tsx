import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQueryClient } from '@tanstack/react-query'
import { toErrorMessage } from 'lib/error'
import { queryKeys } from 'lib/query/keys'
import { MypageOut } from 'types/internal/user'
import { postPaymentChange } from 'api/internal/payment'
import { FetchError } from 'utils/constants/enum'
import { useLoading } from 'components/hooks/useLoading'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import style from './Change.module.scss'
import CurrentBanner from '../CurrentBanner'
import PlanCard from '../PlanCard'
import { plans } from '../plans'

interface Props {
  mypage: MypageOut
}

export default function PaymentChange(props: Props): React.JSX.Element {
  const { mypage } = props

  const router = useRouter()
  const queryClient = useQueryClient()
  const { t } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { toast, handleToast } = useToast()
  const [activeName, setActiveName] = useState<string>('')

  const currentPlanName = mypage.plan
  const isChanged = activeName !== '' && activeName !== currentPlanName

  const handleBack = () => router.push('/setting/payment')

  const handleSubmit = async () => {
    handleLoading(true)
    const ret = await postPaymentChange({ plan: activeName })
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(toErrorMessage(ret.error, FetchError.Post), true)
      return
    }
    setActiveName('')
    handleToast(t('setting.payment.changed'), false)
    await queryClient.invalidateQueries({ queryKey: queryKeys.settingMypage })
  }

  return (
    <Main metaTitle={t('setting.payment.changeTitle')} toast={toast}>
      <div className={style.change}>
        <CurrentBanner planName={currentPlanName} />

        <div className={style.plans}>
          {plans.map((plan) => (
            <PlanCard
              key={plan.name}
              plan={plan}
              active={activeName === plan.name}
              onClick={() => setActiveName(plan.name)}
              current={plan.name === currentPlanName}
              showPurchase={false}
            />
          ))}
        </div>

        <div className={style.actions}>
          <Button color="green" name={t('setting.button.change')} disabled={!isChanged} loading={loading} onClick={handleSubmit} />
          <Button color="blue" name={t('setting.button.cancel')} onClick={handleBack} />
        </div>
      </div>
    </Main>
  )
}
