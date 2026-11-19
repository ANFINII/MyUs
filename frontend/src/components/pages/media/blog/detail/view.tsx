import { useTranslation } from 'react-i18next'
import { BlogDetailOut } from 'types/internal/media/output'
import { MediaPath } from 'utils/constants/enum'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import BlogArticle from 'components/widgets/BlogArticle'
import MediaDetail from 'components/widgets/Media/Detail'
import MediaDetailCommon from 'components/widgets/Media/Detail/Common'
import Paywall from 'components/widgets/Paywall'

interface Props {
  data: BlogDetailOut
}

export default function BlogDetail(props: Props): React.JSX.Element {
  const { data } = props
  const { detail, list, series } = data
  const { publish, richtext, paidText, product, isPurchased, isPromotion, ...other } = detail

  const { t } = useTranslation()
  const { toast, handleToast } = useToast()

  const isLocked = product !== null && paidText === '' && !isPurchased

  return (
    <Main metaTitle="Blog" toast={toast}>
      <MediaDetail publish={publish}>
        <BlogArticle richtext={richtext} paidText={paidText} isPromotion={isPromotion} />
        {isLocked && product !== null && <Paywall title={t('media.blog.paywallTitle')} notice={t('media.blog.paywallNotice')} product={product} handleToast={handleToast} />}
        <Divide />
        <MediaDetailCommon media={{ mediaPath: MediaPath.Blog, ...other }} list={list} series={series} handleToast={handleToast} />
      </MediaDetail>
    </Main>
  )
}
