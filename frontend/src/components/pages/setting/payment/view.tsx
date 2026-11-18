import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQueryClient } from '@tanstack/react-query'
import { errorMessage } from 'lib/error'
import { queryKeys } from 'lib/query/keys'
import { PaymentPlanOut, PaymentSellerOut, PaymentSubscriptionOut } from 'types/internal/payment'
import { MypageOut } from 'types/internal/user'
import { postPaymentCancelRevoke, postPaymentCheckout, postPaymentMethod, postPaymentSellerOnboard } from 'api/internal/payment'
import { FetchError } from 'utils/constants/enum'
import { toLocale } from 'utils/functions/convertEnum'
import { useLoading } from 'components/hooks/useLoading'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Link from 'components/parts/Link'
import CurrentBanner from './CurrentBanner'
import style from './Payment.module.scss'
import PlanCard from './PlanCard'
import { plans } from './plans'

interface Props {
  mypage: MypageOut
  subscription: PaymentSubscriptionOut
  planPrices: PaymentPlanOut[]
  seller: PaymentSellerOut
}

export default function Payment(props: Props): React.JSX.Element {
  const { mypage, subscription, planPrices, seller } = props

  const router = useRouter()
  const queryClient = useQueryClient()
  const { t, i18n } = useTranslation()
  const { loading, handleLoading } = useLoading()
  const { toast, handleToast } = useToast()
  const [isMethodLoading, setIsMethodLoading] = useState<boolean>(false)
  const [isSellerLoading, setIsSellerLoading] = useState<boolean>(false)
  const [selectedPlan, setSelectedPlan] = useState<string>('')

  const currentPlan = mypage.plan
  const purchasable = plans.filter((plan) => plan.name !== 'Free')
  const priceMap = new Map(planPrices.map((p) => [p.name, p.price]))
  const isPaid = currentPlan !== 'Free'
  const isCanceled = isPaid && subscription.isCanceled
  const isPastDue = isPaid && subscription.isPastDue
  const cancelNotice = isCanceled ? t('setting.payment.cancelScheduled', { periodEnd: new Date(subscription.periodEnd).toLocaleDateString(i18n.language) }) : ''
  const notice = isPastDue ? t('setting.payment.pastDue') : cancelNotice
  const sellerPending = seller.isRegistered ? t('setting.payment.seller.pending') : t('setting.payment.seller.description')
  const sellerNotice = seller.isEnabled ? t('setting.payment.seller.enabled') : sellerPending

  const handleChange = () => router.push('/setting/payment/change')

  const handlePurchase = async (plan: string) => {
    setSelectedPlan(plan)
    const locale = toLocale(router.locale)
    const ret = await postPaymentCheckout({ plan, locale })
    if (ret.isErr()) {
      setSelectedPlan('')
      handleToast(errorMessage(ret.error, FetchError.Post), true)
      return
    }
    router.push(ret.value.url)
  }

  const handleMethod = async () => {
    setIsMethodLoading(true)
    const locale = toLocale(router.locale)
    const ret = await postPaymentMethod({ locale })
    if (ret.isErr()) {
      setIsMethodLoading(false)
      handleToast(errorMessage(ret.error, FetchError.Post), true)
      return
    }
    router.push(ret.value.url)
  }

  const handleSellerOnboard = async () => {
    setIsSellerLoading(true)
    const locale = toLocale(router.locale)
    const ret = await postPaymentSellerOnboard({ locale })
    if (ret.isErr()) {
      setIsSellerLoading(false)
      handleToast(errorMessage(ret.error, FetchError.Post), true)
      return
    }
    router.push(ret.value.url)
  }

  const handleRevoke = async () => {
    handleLoading(true)
    const ret = await postPaymentCancelRevoke()
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(errorMessage(ret.error, FetchError.Post), true)
      return
    }
    handleToast(t('setting.payment.revoked'), false)
    await queryClient.invalidateQueries({ queryKey: queryKeys.settingMypage })
    await queryClient.invalidateQueries({ queryKey: queryKeys.paymentSubscription })
  }

  return (
    <Main metaTitle={t('setting.payment.title')} toast={toast}>
      <div className={style.payment}>
        <CurrentBanner planName={currentPlan} notice={notice} />

        <div className={style.plans}>
          {purchasable.map((plan) => (
            <PlanCard
              key={plan.name}
              plan={plan}
              price={priceMap.get(plan.name)}
              active={currentPlan === plan.name}
              disabled={isPaid}
              loading={selectedPlan === plan.name}
              onPurchase={handlePurchase}
            />
          ))}
        </div>

        <p className={style.currency}>
          {isPaid ? (
            t('setting.payment.currencyBySubscription')
          ) : (
            <>
              {t('setting.payment.currencyByCountry')}
              <Link href="/setting/profile/edit" className={style.currency_link}>
                {t('setting.payment.changeCountry')}
              </Link>
            </>
          )}
        </p>

        {isCanceled && (
          <div className={style.actions}>
            <Button color="green" name={t('setting.payment.revoke')} loading={loading} onClick={handleRevoke} />
            <Button color="blue" name={t('setting.payment.method')} loading={isMethodLoading} onClick={handleMethod} />
          </div>
        )}

        {isPaid && !isCanceled && (
          <div className={style.actions}>
            <Button color="green" name={t('setting.payment.change')} onClick={handleChange} />
            <Button color="blue" name={t('setting.payment.method')} loading={isMethodLoading} onClick={handleMethod} />
          </div>
        )}

        {(seller.isAvailable || seller.isRegistered) && (
          <section className={style.seller}>
            <h2 className={style.seller_title}>{t('setting.payment.seller.title')}</h2>
            <p className={style.seller_notice}>{sellerNotice}</p>
            {!seller.isEnabled && (
              <Button
                color="blue"
                name={seller.isRegistered ? t('setting.payment.seller.continue') : t('setting.payment.seller.register')}
                loading={isSellerLoading}
                onClick={handleSellerOnboard}
              />
            )}
          </section>
        )}

        <footer className={style.footer}>
          <p className={style.notice}>{t('setting.payment.renewalNotice')}</p>
          <nav className={style.links}>
            <Link href="/menu/commerce" className={style.link}>
              {t('menu.commerce.title')}
            </Link>
            <Link href="/menu/privacy" className={style.link}>
              {t('menu.privacy.title')}
            </Link>
            <Link href="/menu/userpolicy" className={style.link}>
              {t('menu.userpolicy.title')}
            </Link>
          </nav>
        </footer>
      </div>
    </Main>
  )
}
