import { useTranslation } from 'react-i18next'
import { errorMessage } from 'lib/error'
import { Product } from 'types/internal/payment'
import { postPaymentProductCheckout } from 'api/internal/payment'
import { FetchError } from 'utils/constants/enum'
import { toLocale } from 'utils/functions/convertEnum'
import { formatPrice } from 'utils/functions/price'
import { useLoading } from 'components/hooks/useLoading'
import { useRouter } from 'components/hooks/useRouter'
import { useUser } from 'components/hooks/useUser'
import Button from 'components/parts/Button'
import LoginRequired from 'components/widgets/Status/LoginRequired'
import style from './Paywall.module.scss'

interface Props {
  title: string
  label?: string
  notice: string
  product: Product
  handleToast: (content: string, isError: boolean) => void
}

export default function Paywall(props: Props): React.JSX.Element {
  const { title, label, notice, product, handleToast } = props

  const router = useRouter()
  const { t, i18n } = useTranslation()
  const { user } = useUser()
  const { loading, handleLoading } = useLoading()

  const handlePurchase = async () => {
    handleLoading(true)
    const locale = toLocale(router.locale)
    const ret = await postPaymentProductCheckout({ productUlid: product.ulid, locale })
    if (ret.isErr()) {
      handleLoading(false)
      handleToast(errorMessage(ret.error, FetchError.Post), true)
      return
    }
    router.push(ret.value.url)
  }

  return (
    <section className={style.paywall}>
      <p className={style.paywall_title}>{title}</p>
      {label && <p className={style.paywall_label}>{label}</p>}
      <p className={style.paywall_price}>{formatPrice(product.price.amount, product.price.currency, i18n.language)}</p>
      {user.isActive ? <Button color="green" name={t('media.purchase')} loading={loading} onClick={handlePurchase} /> : <LoginRequired />}
      <p className={style.paywall_notice}>{notice}</p>
    </section>
  )
}
