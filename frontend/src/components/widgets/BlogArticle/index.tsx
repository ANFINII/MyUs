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
    if (!(e.target instanceof Element)) return
    const button = e.target.closest('[data-code-copy]')
    if (!(button instanceof HTMLButtonElement)) return
    try {
      await navigator.clipboard.writeText(button.nextElementSibling?.textContent ?? '')
    } catch {
      return
    }
    button.setAttribute('data-copied', '')
    button.title = t('media.blog.codeCopied')
    setTimeout(() => {
      button.removeAttribute('data-copied')
      button.title = t('action.copy')
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
