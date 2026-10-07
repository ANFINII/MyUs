import { useRef } from 'react'
import { useTranslation } from 'react-i18next'
import style from './LinkInput.module.scss'

interface Props {
  onSubmit: (url: string) => void
  onCancel: () => void
}

export default function LinkInput(props: Props): React.JSX.Element {
  const { onSubmit, onCancel } = props

  const { t } = useTranslation()

  const inputRef = useRef<HTMLInputElement>(null)

  const handleSubmit = () => {
    const url = inputRef.current?.value.trim()
    if (!url) return
    onSubmit(url)
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      handleSubmit()
    }
    if (e.key === 'Escape') {
      onCancel()
    }
  }

  return (
    <div className={style.link}>
      <input ref={inputRef} type="url" className={style.field} placeholder={t('textEditor.urlPlaceholder')} autoFocus onKeyDown={handleKeyDown} />
      <button type="button" className={style.submit} onClick={handleSubmit}>
        {t('textEditor.insert')}
      </button>
      <button type="button" className={style.cancel} onClick={onCancel}>
        ✕
      </button>
    </div>
  )
}
