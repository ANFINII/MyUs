import { MouseEvent } from 'react'
import { useTranslation } from 'react-i18next'
import { addCodeCopyButtons } from 'utils/functions/code'
import Alert from 'components/parts/Alert'
import FormatHtml from 'components/parts/FormatHtml'
import style from './BlogArticle.module.scss'

const COPIED_MS = 2000

interface Props {
  richtext: string
  paidText: string
  isPromotion: boolean
}

export default function BlogArticle(props: Props): React.JSX.Element {
  const { richtext, paidText, isPromotion } = props

  const { t } = useTranslation()

  const handleCopy = async (e: MouseEvent<HTMLDivElement>) => {
    const button = e.target
    if (!(button instanceof HTMLButtonElement) || !button.hasAttribute('data-code-copy')) return
    try {
      await navigator.clipboard.writeText(button.nextElementSibling?.textContent ?? '')
    } catch {
      return
    }
    button.textContent = t('media.blog.codeCopied')
    setTimeout(() => {
      button.textContent = t('action.copy')
    }, COPIED_MS)
  }

  return (
    <div className={style.article} onClick={handleCopy}>
      {isPromotion && <Alert type="info">{t('media.blog.promotion')}</Alert>}
      <FormatHtml content={addCodeCopyButtons(richtext, t('action.copy'))} isSponsored={isPromotion} />
      {paidText !== '' && (
        <>
          <p className={style.paid_line}>{t('media.blog.paidLine')}</p>
          <FormatHtml content={addCodeCopyButtons(paidText, t('action.copy'))} isSponsored={isPromotion} />
        </>
      )}
    </div>
  )
}
