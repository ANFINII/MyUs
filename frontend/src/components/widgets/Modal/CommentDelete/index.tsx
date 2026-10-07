import { useTranslation } from 'react-i18next'
import { Author } from 'types/internal/user'
import { useDatetime } from 'components/hooks/useDatetime'
import Avatar from 'components/parts/Avatar'
import Modal from 'components/parts/Modal'
import HStack from 'components/parts/Stack/Horizontal'
import style from './CommentDelete.module.scss'

export interface Props {
  open: boolean
  onClose: () => void
  onAction: () => void
  loading?: boolean
  comment: {
    author: Author
    created: Date
    text: string
  }
}

export default function CommentDeleteModal(props: Props): React.JSX.Element {
  const { open, onClose, onAction, loading, comment } = props
  const { author, created, text } = comment

  const { t } = useTranslation()
  const { formatDatetime } = useDatetime()

  return (
    <Modal
      open={open}
      onClose={onClose}
      title={t('modal.commentDelete.title')}
      actions={[
        { name: t('action.delete'), color: 'red', loading, onClick: onAction },
        { name: t('action.cancel'), color: 'white', onClick: onClose },
      ]}
    >
      <div className="mb_8">{t('modal.commentDelete.confirm')}</div>
      <HStack gap="4" className={style.comment}>
        <Avatar src={author.avatar} title={author.nickname} size="40" color="grey" />
        <div>
          <div className={style.comment_info}>
            <span className="mr_4">{author.nickname}</span>
            <time>{formatDatetime(created)}</time>
          </div>
          <p className={style.text}>{text}</p>
        </div>
      </HStack>
    </Modal>
  )
}
