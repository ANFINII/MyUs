import { useTranslation } from 'react-i18next'
import { BlogDetailOut } from 'types/internal/media/output'
import { MediaPath } from 'utils/constants/enum'
import { buildToc } from 'utils/functions/toc'
import { useToast } from 'components/hooks/useToast'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import BlogArticle from 'components/widgets/BlogArticle'
import BlogToc from 'components/widgets/BlogToc'
import BlogTocMobile from 'components/widgets/BlogToc/Mobile'
import MediaDetail from 'components/widgets/Media/Detail'
import MediaDetailCommon from 'components/widgets/Media/Detail/Common'
import MediaSeriesPager from 'components/widgets/Media/Series/Pager'
import Paywall from 'components/widgets/Paywall'
import style from './BlogDetail.module.scss'

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
  const article = buildToc(richtext, paidText)

  return (
    <Main metaTitle="Blog" toast={toast}>
      <MediaDetail publish={publish}>
        <div className={style.blog_body}>
          <div className={style.main}>
            <h1 className={style.title}>{other.title}</h1>
            {article.headings.length > 0 && <BlogTocMobile headings={article.headings} className={style.mobile_toc} />}
            <BlogArticle richtext={article.richtext} paidText={article.paidText} isPromotion={isPromotion} />
            {isLocked && product !== null && <Paywall title={t('media.blog.paywallTitle')} notice={t('media.blog.paywallNotice')} product={product} handleToast={handleToast} />}
            <MediaSeriesPager
              series={series}
              ulid={other.ulid}
              mediaPath={MediaPath.Blog}
              prevLabel={t('media.blog.prevArticle')}
              nextLabel={t('media.blog.nextArticle')}
              className={style.pager}
            />
          </div>
          <aside className={style.side}>{article.headings.length > 0 && <BlogToc headings={article.headings} className={style.toc} />}</aside>
        </div>
        <Divide />
        <MediaDetailCommon media={{ mediaPath: MediaPath.Blog, ...other }} list={list} series={series} handleToast={handleToast} />
      </MediaDetail>
    </Main>
  )
}
