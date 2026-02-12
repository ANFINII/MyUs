import { useEffect, useRef } from 'react'
import style from './LinkInput.module.scss'

interface Props {
  onSubmit: (url: string) => void
  onCancel: () => void
}

export default function LinkInput(props: Props): React.JSX.Element {
  const { onSubmit, onCancel } = props

  const inputRef = useRef<HTMLInputElement>(null)
  useEffect(() => inputRef.current?.focus(), [])

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
      <input ref={inputRef} type="url" className={style.field} placeholder="URLを入力" onKeyDown={handleKeyDown} />
      <button type="button" className={style.submit} onClick={handleSubmit}>
        挿入
      </button>
      <button type="button" className={style.cancel} onClick={onCancel}>
        ✕
      </button>
    </div>
  )
}
