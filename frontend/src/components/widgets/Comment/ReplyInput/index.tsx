import { ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import { UserMe } from 'types/internal/user'
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

export default function ReplyInput(props: Props): React.JSX.Element {
  const { user, value, open, onChange, onSubmit, onCancel } = props

  const { t } = useTranslation()

  return (
    <>
      {open && (
        <HStack gap="4" align="start">
          <AvatarLink size="s" src={user.avatar} ulid={user.ulid} title={user.nickname} className="m_2" />
          <VStack gap="4" className="w_full">
            <TextareaLine name="text" placeholder={t('comment.placeholder')} value={value} onChange={onChange} onSubmit={onSubmit} />
            <HStack gap="4" justify="end">
              <Button size="s" name={t('action.cancel')} onClick={onCancel} />
              <Button size="s" color="blue" name={t('action.reply')} disabled={value.trim() === ''} onClick={onSubmit} />
            </HStack>
          </VStack>
        </HStack>
      )}
    </>
  )
}
