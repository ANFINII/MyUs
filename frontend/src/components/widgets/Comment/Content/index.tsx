import { useState, useRef } from 'react'
import { Comment } from 'types/internal/comment'
import { postCommentLike } from 'api/internal/media/detail'
import { formatDatetime } from 'utils/functions/datetime'
import AvatarLink from 'components/parts/Avatar/Link'
import CountLike from 'components/parts/Count/Like'
import IconEdit from 'components/parts/Icon/Edit'
import IconTrash from 'components/parts/Icon/Trash'
import Horizontal from 'components/parts/Stack/Horizontal'
import Vertical from 'components/parts/Stack/Vertical'
import CommentDeleteModal from 'components/widgets/Modal/CommentDelete'
import style from './CommentContent.module.scss'
import CommentAction from '../Action'
import CommentReply from '../Reply'
import CommentThread from '../Thread'

export interface Props {
  comment: Comment
  disabled: boolean
  isActive: boolean
  onLikeComment: (commentId: number) => void
}

export default function CommentContent(props: Props): JSX.Element {
  const { comment, disabled, isActive, onLikeComment } = props
  const { author, created, text } = comment

  const [isMenu, setIsMenu] = useState<boolean>(false)
  const [isModal, setIsModal] = useState<boolean>(false)
  const actionButtonRef = useRef<HTMLButtonElement>(null)

  const [isReplyView, setIsReplyView] = useState<boolean>(false)
  const [isThreadView, setIsThreadView] = useState<boolean>(false)

  const handleReplyView = () => setIsReplyView(!isReplyView)
  const handleThreadView = () => setIsThreadView(!isThreadView)

  const handleLike = async (commentId: number): Promise<void> => {
    const ret = await postCommentLike(commentId)
    if (ret.isErr()) return
    onLikeComment(commentId)
  }

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
    <Horizontal>
      <Horizontal gap="4" className={style.comment}>
        <AvatarLink src={author.avatar} size="40" nickname={author.nickname} />
        <Vertical gap="2">
          <div className={style.comment_info}>
            <span className="mr_4">{author.nickname}</span>
            <time>{formatDatetime(created)}</time>
          </div>
          <p className={style.text}>{text}</p>
          <Horizontal gap="4" className="fs_12">
            <CountLike isLike={comment.isCommentLike} disable={!isActive} like={comment.totalLike} onClick={() => handleLike(comment.id)} />
            <CommentReply isView={isReplyView} onClick={handleReplyView} />
            <CommentThread isView={isThreadView} count={comment.replyCount || 0} onClick={handleThreadView} />
            <div className={style.comment_aria_list_space} />
            <div id={`reply_aria_list_${comment.id}`} className={style.comment_aria_list_5} />
          </Horizontal>
        </Vertical>
      </Horizontal>
      <CommentAction open={isMenu} onMenu={handleMenu} actionRef={actionButtonRef} disabled={disabled} actionItems={actionItems} />
      <CommentDeleteModal open={isModal} onClose={handleModal} onAction={() => {}} comment={comment} />
    </Horizontal>
  )
}
