import { useState, useRef } from 'react'
import { Comment } from 'types/internal/comment'
import { formatDatetime } from 'utils/functions/datetime'
import AvatarLink from 'components/parts/Avatar/Link'
import IconDots from 'components/parts/Icon/Dots'
import IconEdit from 'components/parts/Icon/Edit'
import IconTrash from 'components/parts/Icon/Trash'
import Horizontal from 'components/parts/Stack/Horizontal'
import ActionList from 'components/widgets/Comment/ActionList'
import CommentDeleteModal from 'components/widgets/Modal/CommentDelete'
import style from './CommentContent.module.scss'

export interface Props {
  comment: Comment
  nickname?: string
}

export default function CommentContent(props: Props): JSX.Element {
  const { comment, nickname } = props
  const { author, created, text } = comment

  const [isMenu, setIsMenu] = useState<boolean>(false)
  const [isModal, setIsModal] = useState<boolean>(false)
  const actionButtonRef = useRef<HTMLButtonElement>(null)

  const handleMenu = () => setIsMenu(!isMenu)
  const handleModal = () => setIsModal(!isModal)

  const handleEdit = () => {
    // TODO: Implement edit functionality
  }

  const handleDelete = () => setIsModal(true)

  const actionItems = [
    { icon: <IconEdit size="16" />, label: '編集', onClick: handleEdit },
    { icon: <IconTrash size="16" />, label: '削除', onClick: handleDelete, danger: true },
  ]

  return (
    <>
      <Horizontal>
        <Horizontal gap="4" className={style.comment}>
          <AvatarLink src={author.avatar} size="40" nickname={author.nickname} />
          <div>
            <div className={style.comment_info}>
              <span className="mr_4">{author.nickname}</span>
              <time>{formatDatetime(created)}</time>
            </div>
            <p className={style.text}>{text}</p>
          </div>
        </Horizontal>
        {comment.author.nickname === nickname && (
          <div className={style.action_wrap}>
            <button ref={actionButtonRef} className={style.action_button} onClick={handleMenu}>
              <IconDots size="18" />
            </button>
            <div className={style.action_list}>
              <ActionList triggerRef={actionButtonRef} open={isMenu} onClose={handleMenu} items={actionItems} />
            </div>
          </div>
        )}
      </Horizontal>
      <CommentDeleteModal open={isModal} onClose={handleModal} onAction={() => {}} comment={comment} />
    </>
  )
}
