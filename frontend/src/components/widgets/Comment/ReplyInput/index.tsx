import { ChangeEvent } from 'react'
import { UserMe } from 'types/internal/auth'
import AvatarLink from 'components/parts/Avatar/Link'
import Button from 'components/parts/Button'
import TextareaLine from 'components/parts/Input/Textarea/Line'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'

interface Props {
  user: UserMe
  value: string
  open: boolean
  onChange?: (e: ChangeEvent<HTMLTextAreaElement>) => void
  onSubmit: () => void
  onCancel: () => void
}

export default function ReplyInput(props: Props): JSX.Element {
  const { user, value, open, onChange, onSubmit, onCancel } = props

  return (
    <>
      {open && (
        <HStack gap="4">
          <AvatarLink src={user.avatar} size="s" nickname={user.nickname} className="m_2" />
          <VStack gap="4" className="w_full">
            <TextareaLine name="text" placeholder="コメント入力" value={value} onChange={onChange} />
            <HStack gap="4" justify="end">
              <Button size="s" name="キャンセル" onClick={onCancel} />
              <Button size="s" color="blue" name="返信" disabled={value.trim() === ''} onClick={onSubmit} />
            </HStack>
          </VStack>
        </HStack>
      )}
    </>
  )
}
