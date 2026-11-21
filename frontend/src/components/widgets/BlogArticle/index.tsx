import { KeyboardEvent, MouseEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { addHeadingLinks, decorateCodeBlocks } from 'utils/functions/article'
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
  const [zoomSrc, setZoomSrc] = useState('')

  const decorate = (html: string) => addHeadingLinks(decorateCodeBlocks(html, t('media.blog.codeCopy')), t('media.blog.headingLink'))

  const showCopied = (button: HTMLButtonElement) => {
    button.setAttribute('data-copied', '')
    setTimeout(() => button.removeAttribute('data-copied'), COPIED_MS)
  }

  const copyText = async (button: HTMLButtonElement, text: string) => {
    try {
      await navigator.clipboard.writeText(text)
    } catch {
      return
    }
    showCopied(button)
  }

  const handleClick = async (e: MouseEvent<HTMLDivElement>) => {
    if (!(e.target instanceof Element)) return
    if (e.target instanceof HTMLImageElement) {
      setZoomSrc(e.target.src)
      return
    }
    const button = e.target.closest('button')
    if (!button) return
    if (button.hasAttribute('data-code-copy')) {
      await copyText(button, button.parentElement?.querySelector('pre')?.textContent ?? '')
      return
    }
    if (button.hasAttribute('data-heading-link')) {
      const id = button.parentElement?.id ?? ''
      await copyText(button, `${window.location.origin}${window.location.pathname}#${id}`)
    }
  }

  const handleZoomKey = (e: KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'Escape') setZoomSrc('')
  }

  return (
    <div className={style.article} onClick={handleClick}>
      {isPromotion && <Alert type="info">{t('media.blog.promotion')}</Alert>}
      <FormatHtml content={decorate(richtext)} isSponsored={isPromotion} />
      {paidText !== '' && (
        <>
          <p className={style.paid_line}>{t('media.blog.paidLine')}</p>
          <FormatHtml content={decorate(paidText)} isSponsored={isPromotion} />
        </>
      )}
      {zoomSrc !== '' && (
        <div className={style.zoom} role="dialog" aria-modal="true" onClick={() => setZoomSrc('')} onKeyDown={handleZoomKey}>
          <img src={zoomSrc} alt="" className={style.zoom_image} />
          <button type="button" className={style.zoom_close} aria-label={t('action.close')} autoFocus>
            ×
          </button>
        </div>
      )}
    </div>
  )
}
