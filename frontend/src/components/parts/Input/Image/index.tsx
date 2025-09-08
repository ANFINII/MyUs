import { ChangeEvent, useRef } from 'react'

interface Props {
  id: string
  className?: string
  icon?: React.ReactNode
  onChange?: (files: File | File[]) => void
}

export default function InputImage(props: Props): React.JSX.Element {
  const { id, className = '', icon, onChange } = props

  const inputEl = useRef<HTMLInputElement>(null)

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files[0] && onChange) onChange(files[0])
  }

  return (
    <label htmlFor={id} className={className}>
      {icon}
      <input id={id} ref={inputEl} type="file" accept="image/*" onChange={handleChange} />
    </label>
  )
}
