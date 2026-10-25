import { useState, ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import { Option } from 'types/internal/other'
import Select from 'components/parts/Select'
import style from './ImageInput.module.scss'

const MIN_WIDTH = 50
const MAX_WIDTH = 1200

export interface ImageValues {
  width?: number
  rounded: string
}

interface Props {
  values?: ImageValues
  isEdit?: boolean
  onSubmit: (values: ImageValues) => void
  onCancel: () => void
}

export default function ImageInput(props: Props): React.JSX.Element {
  const { values, isEdit = false, onSubmit, onCancel } = props

  const { t } = useTranslation()

  const [width, setWidth] = useState<string>(values?.width ? String(Math.round(values.width)) : '')
  const [rounded, setRounded] = useState<string>(values?.rounded ?? '')

  const roundedOptions: Option[] = [
    { label: t('textEditor.roundedNone'), value: '' },
    { label: t('textEditor.roundedSmall'), value: 's' },
    { label: t('textEditor.roundedMedium'), value: 'm' },
    { label: t('textEditor.roundedLarge'), value: 'l' },
  ]

  const handleWidth = (e: ChangeEvent<HTMLInputElement>) => setWidth(e.target.value)
  const handleRounded = (e: ChangeEvent<HTMLSelectElement>) => setRounded(e.target.value)

  const handleSubmit = () => {
    const value = width ? Math.min(Math.max(Math.round(Number(width)), MIN_WIDTH), MAX_WIDTH) : undefined
    onSubmit({ width: value, rounded })
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
      <input
        type="number"
        min={MIN_WIDTH}
        max={MAX_WIDTH}
        value={width}
        className={style.field}
        placeholder={t('textEditor.widthPlaceholder')}
        autoFocus={!isEdit}
        onChange={handleWidth}
        onKeyDown={handleKeyDown}
      />
      <span className={style.unit}>px</span>
      <span className={style.unit}>{t('textEditor.rounded')}</span>
      <Select value={rounded} options={roundedOptions} className={style.select} onChange={handleRounded} />
      <button type="button" className={style.submit} onClick={handleSubmit}>
        {isEdit ? t('action.update') : t('textEditor.insert')}
      </button>
      <button type="button" className={style.cancel} onClick={onCancel}>
        ✕
      </button>
    </div>
  )
}
