import { useTranslation } from 'react-i18next'
import Alert from 'components/parts/Alert'
import FormatHtml from 'components/parts/FormatHtml'
import style from './BlogArticle.module.scss'

interface Props {
  richtext: string
  paidText: string
  isPromotion: boolean
}

export default function BlogArticle(props: Props): React.JSX.Element {
  const { richtext, paidText, isPromotion } = props

  const { t } = useTranslation()

  return (
    <div className={style.article}>
      {isPromotion && <Alert type="info">{t('media.blog.promotion')}</Alert>}
      <FormatHtml content={richtext} isSponsored={isPromotion} />
      {paidText !== '' && (
        <>
          <p className={style.paid_line}>{t('media.blog.paidLine')}</p>
          <FormatHtml content={paidText} isSponsored={isPromotion} />
        </>
      )}
    </div>
  )
}
