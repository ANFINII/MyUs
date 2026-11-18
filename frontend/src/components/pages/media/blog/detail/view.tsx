import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { errorMessage } from 'lib/error'
import { BlogDetailOut } from 'types/internal/media/output'
import { postPaymentBlogCheckout } from 'api/internal/payment'
import { FetchError, MediaPath } from 'utils/constants/enum'
import { toLocale } from 'utils/functions/convertEnum'
import { formatPrice } from 'utils/functions/price'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Divide from 'components/parts/Divide'
import BlogArticle from 'components/widgets/BlogArticle'
import MediaDetail from 'components/widgets/Media/Detail'
import MediaDetailCommon from 'components/widgets/Media/Detail/Common'
import LoginRequired from 'components/widgets/Status/LoginRequired'
import style from './Detail.module.scss'

interface Props {
  data: BlogDetailOut
}

export default function BlogDetail(props: Props): React.JSX.Element {
  const { data } = props
  const { detail, list, series } = data
  const { publish, richtext, paidText, price, isPurchased, isPromotion, ...other } = detail

  const router = useRouter()
  const { t, i18n } = useTranslation()
  const { user } = useUser()
  const { toast, handleToast } = useToast()
  const [isPurchaseLoading, setIsPurchaseLoading] = useState<boolean>(false)

  const isLocked = price.amount > 0 && paidText === '' && !isPurchased

  const handlePurchase = async () => {
    setIsPurchaseLoading(true)
    const locale = toLocale(router.locale)
    const ret = await postPaymentBlogCheckout({ blogUlid: detail.ulid, locale })
    if (ret.isErr()) {
      setIsPurchaseLoading(false)
      handleToast(errorMessage(ret.error, FetchError.Post), true)
      return
    }
    router.push(ret.value.url)
  }

  return (
    <Main metaTitle="Blog" toast={toast}>
      <MediaDetail publish={publish}>
        <BlogArticle richtext={richtext} paidText={paidText} isPromotion={isPromotion} />
        {isLocked && (
          <section className={style.paywall}>
            <p className={style.paywall_title}>{t('media.blog.paywallTitle')}</p>
            <p className={style.paywall_price}>{formatPrice(price.amount, price.currency, i18n.language)}</p>
            {user.isActive ? <Button color="green" name={t('media.blog.purchase')} loading={isPurchaseLoading} onClick={handlePurchase} /> : <LoginRequired />}
            <p className={style.paywall_notice}>{t('media.blog.paywallNotice')}</p>
          </section>
        )}
        <Divide />
        <MediaDetailCommon media={{ mediaPath: MediaPath.Blog, ...other }} list={list} series={series} handleToast={handleToast} />
      </MediaDetail>
    </Main>
  )
}
