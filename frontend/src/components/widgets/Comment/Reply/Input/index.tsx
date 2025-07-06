import { Author } from 'types/internal/media'
import Avatar from 'components/parts/Avatar'
import Button from 'components/parts/Button'
import TextareaLine from 'components/parts/Input/Textarea/Line'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import style from './ReplyInput.module.scss'

interface Props {
  author: Author
  value: string
  open: boolean
  onChange?: (e: React.ChangeEvent<HTMLTextAreaElement>) => void
  onSubmit: () => void
  onCancel: () => void
}

export default function ReplyInput(props: Props): JSX.Element {
  const { author, value, open, onChange, onSubmit, onCancel } = props

  return (
    <>
      {open && (
        <HStack gap="4">
          <Avatar src={author.avatar} title={author.nickname} size="36" color="grey" className={style.avatar} />
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
