import { useTranslation } from 'react-i18next'
import { Author } from 'types/internal/user'
import { sanitizeHtml } from 'utils/functions/sanitize'
import { useDatetime } from 'components/hooks/useDatetime'
import Avatar from 'components/parts/Avatar'
import Modal from 'components/parts/Modal'
import HStack from 'components/parts/Stack/Horizontal'
import style from './MessageDelete.module.scss'

interface Props {
  open: boolean
  onClose: () => void
  onAction: () => void
  message: {
    author: Author
    created: Date
    text: string
  }
}

export default function MessageDeleteModal(props: Props): React.JSX.Element {
  const { open, onClose, onAction, message } = props
  const { author, created, text } = message

  const { t } = useTranslation()
  const { formatDatetime } = useDatetime()

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={t('modal.messageDelete.title')}
      actions={[
        { name: t('action.delete'), color: 'red', onClick: onAction },
        { name: t('action.cancel'), color: 'white', onClick: onClose },
      ]}
    >
      <div className="mb_8">{t('modal.messageDelete.confirm')}</div>
      <HStack gap="4" className={style.message}>
        <Avatar src={author.avatar} title={author.nickname} size="40" color="grey" />
        <div>
          <div className={style.message_info}>
            <span className="mr_4">{author.nickname}</span>
            <time>{formatDatetime(created)}</time>
          </div>
          <p className={style.text} dangerouslySetInnerHTML={{ __html: sanitizeHtml(text) }} />
        </div>
      </HStack>
    </Modal>
  )
}
