import { ChangeEvent } from 'react'
import { useTranslation } from 'react-i18next'
import Button from 'components/parts/Button'
import TextareaLine from 'components/parts/Input/Textarea/Line'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'

interface Props {
  value: string
  loading?: boolean
  onChange?: (e: ChangeEvent<HTMLTextAreaElement>) => void
  onSubmit: () => void
  onCancel: () => void
}

export default function CommentUpdate(props: Props): React.JSX.Element {
  const { value, loading, onChange, onSubmit, onCancel } = props

  const { t } = useTranslation()

  const handleSubmit = () => {
    if (loading || value.trim() === '') return
    onSubmit()
  }

  return (
    <VStack gap="4">
      <TextareaLine name="text" placeholder={t('comment.placeholder')} autoFocus value={value} onChange={onChange} onSubmit={handleSubmit} />
      <HStack gap="4" justify="end">
        <Button size="s" name={t('action.cancel')} onClick={onCancel} />
        <Button size="s" color="green" name={t('action.update')} disabled={value.trim() === ''} loading={loading} onClick={onSubmit} />
      </HStack>
    </VStack>
  )
}
