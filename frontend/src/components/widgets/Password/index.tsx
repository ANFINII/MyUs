import { ChangeEvent } from 'react'
import Input from 'components/parts/Input'

interface Props {
  value?: string
  name: string
  placeholder: string
  error?: string
  onChange?: (e: ChangeEvent<HTMLInputElement>) => void
}

export default function Password(props: Props): React.JSX.Element {
  return <Input type="password" minLength={8} maxLength={16} required {...props} />
}
