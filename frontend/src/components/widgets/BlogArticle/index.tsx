import { useTranslation } from 'react-i18next'
import Alert from 'components/parts/Alert'
import FormatHtml from 'components/parts/FormatHtml'
import style from './BlogArticle.module.scss'

interface Props {
  richtext: string
  isPromotion: boolean
}

export default function BlogArticle(props: Props): React.JSX.Element {
  const { richtext, isPromotion } = props

  const { t } = useTranslation()

  return (
    <div className={style.article}>
      {isPromotion && <Alert type="info">{t('media.blog.promotion')}</Alert>}
      <FormatHtml content={richtext} isSponsored={isPromotion} />
    </div>
  )
}
