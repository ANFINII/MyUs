import { ChangeEvent } from 'react'
import Button from 'components/parts/Button'
import TextareaLine from 'components/parts/Input/Textarea/Line'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'

interface Props {
  value: string
  onChange?: (e: ChangeEvent<HTMLTextAreaElement>) => void
  onSubmit: () => void
  onCancel: () => void
}

export default function CommentUpdate(props: Props): React.JSX.Element {
  const { value, onChange, onSubmit, onCancel } = props

  return (
    <VStack gap="4">
      <TextareaLine name="text" placeholder="コメント入力" focus value={value} onChange={onChange} />
      <HStack gap="4" justify="end">
        <Button size="s" name="キャンセル" onClick={onCancel} />
        <Button size="s" color="green" name="更新" disabled={value.trim() === ''} onClick={onSubmit} />
      </HStack>
    </VStack>
  )
}
