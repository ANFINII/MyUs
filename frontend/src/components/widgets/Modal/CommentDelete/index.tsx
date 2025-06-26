import { Comment } from 'types/internal/comment'
import { formatDatetime } from 'utils/functions/datetime'
import Avatar from 'components/parts/Avatar'
import Modal from 'components/parts/Modal'
import Horizontal from 'components/parts/Stack/Horizontal'
import style from './CommentDelete.module.scss'

export interface Props {
  open: boolean
  onClose: () => void
  onAction: () => void
  loading?: boolean
  comment: Comment
}

export default function CommentDeleteModal(props: Props): JSX.Element {
  const { open, onClose, onAction, loading, comment } = props
  const { author, created, text } = comment

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="コメントの削除"
      actions={[
        { name: '削除', color: 'red', loading, onClick: onAction },
        { name: 'キャンセル', color: 'white', onClick: onClose },
      ]}
    >
      <div className="mb_8">こちらコメントを削除しますか？</div>
      <Horizontal gap="4" className={style.comment}>
        <Avatar src={author.avatar} title={author.nickname} size="40" color="grey" />
        <div>
          <div className={style.comment_info}>
            <span className="mr_4">{author.nickname}</span>
            <time>{formatDatetime(created)}</time>
          </div>
          <p className={style.text}>{text}</p>
        </div>
      </Horizontal>
    </Modal>
  )
}
