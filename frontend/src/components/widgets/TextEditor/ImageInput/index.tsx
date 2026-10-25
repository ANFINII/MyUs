import { useRef } from 'react'
import { useTranslation } from 'react-i18next'
import style from './ImageInput.module.scss'

interface Props {
  onSubmit: (width?: number) => void
  onCancel: () => void
}

export default function ImageInput(props: Props): React.JSX.Element {
  const { onSubmit, onCancel } = props

  const { t } = useTranslation()

  const inputRef = useRef<HTMLInputElement>(null)

  const handleSubmit = () => {
    const width = Number(inputRef.current?.value)
    onSubmit(width > 0 ? width : undefined)
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
    <div className={style.image}>
      <input ref={inputRef} type="number" min="1" className={style.field} placeholder={t('textEditor.widthPlaceholder')} autoFocus onKeyDown={handleKeyDown} />
      <span className={style.unit}>px</span>
      <button type="button" className={style.submit} onClick={handleSubmit}>
        {t('textEditor.insert')}
      </button>
      <button type="button" className={style.cancel} onClick={onCancel}>
        ✕
      </button>
    </div>
  )
}
