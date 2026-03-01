import { Author } from 'types/internal/user'
import { formatDatetime } from 'utils/functions/datetime'
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

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="メッセージの削除"
      actions={[
        { name: '削除', color: 'red', onClick: onAction },
        { name: 'キャンセル', color: 'white', onClick: onClose },
      ]}
    >
      <div className="mb_8">こちらのメッセージを削除しますか？</div>
      <HStack gap="4" className={style.message}>
        <Avatar src={author.avatar} title={author.nickname} size="40" color="grey" />
        <div>
          <div className={style.message_info}>
            <span className="mr_4">{author.nickname}</span>
            <time>{formatDatetime(created)}</time>
          </div>
          <p className={style.text} dangerouslySetInnerHTML={{ __html: text }} />
        </div>
      </HStack>
    </Modal>
  )
}
