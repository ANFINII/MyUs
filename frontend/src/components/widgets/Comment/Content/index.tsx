import { useState, useRef } from 'react'
import clsx from 'clsx'
import { Comment } from 'types/internal/comment'
import { deleteCommentLike, postCommentLike } from 'api/internal/media/detail'
import { formatDatetime } from 'utils/functions/datetime'
import AvatarLink from 'components/parts/Avatar/Link'
import CountLike from 'components/parts/Count/Like'
import IconEdit from 'components/parts/Icon/Edit'
import IconTrash from 'components/parts/Icon/Trash'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import CommentDeleteModal from 'components/widgets/Modal/CommentDelete'
import style from './CommentContent.module.scss'
import CommentAction from '../Action'
import ReplyInput from '../Reply/Input'
import ReplyView from '../Reply/View'
import CommentThread from '../Thread'
import ThreadView from '../Thread/View'
import CommentUpdate from '../Update'

export interface Props {
  comment: Comment
  disabled: boolean
  isActive: boolean
  nickname?: string
}

export default function CommentContent(props: Props): JSX.Element {
  const { comment, disabled, isActive, nickname } = props
  const { id, author, created, text, replys, isCommentLike, totalLike } = comment

  const actionButtonRef = useRef<HTMLButtonElement>(null)
  const [isMenu, setIsMenu] = useState<boolean>(false)
  const [isModal, setIsModal] = useState<boolean>(false)
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const [isReplyView, setIsReplyView] = useState<boolean>(false)
  const [isThreadView, setIsThreadView] = useState<boolean>(false)
  const [isLike, setIsLike] = useState<boolean>(isCommentLike || false)
  const [commentText, setCommentText] = useState<string>('')
  const [replyText, setReplyText] = useState<string>('')

  const handleMenu = () => setIsMenu(!isMenu)
  const handleModal = () => setIsModal(!isModal)
  const handleDelete = () => setIsModal(true)
  const handleEditToggle = () => setIsEdit(!isEdit)
  const handleReplyView = () => setIsReplyView(!isReplyView)
  const handleThreadView = () => setIsThreadView(!isThreadView)
  const handleComment = (e: React.ChangeEvent<HTMLTextAreaElement>): void => setCommentText(e.target.value)
  const handleReply = (e: React.ChangeEvent<HTMLTextAreaElement>): void => setReplyText(e.target.value)

  const handleLike = (commentId: number) => async (): Promise<void> => {
    if (isLike) {
      const ret = await deleteCommentLike(commentId)
      if (ret.isErr()) return
    } else {
      const ret = await postCommentLike(commentId)
      if (ret.isErr()) return
    }
    setIsLike(!isLike)
  }

  const handleEdit = () => {
    if (!isEdit) {
      setCommentText(text)
    }
    handleEditToggle()
  }

  const handleUpdate = (commentId: number, text: string) => () => {
    console.log(commentId, text)
    handleEditToggle()
  }

  const handleReplyInput = (commentId: number, text: string) => () => {
    console.log(commentId, text)
    setReplyText('')
  }

  const handleReplyCancel = () => {
    setReplyText('')
    handleReplyView()
  }

  const actionItems = [
    { icon: <IconEdit size="16" />, label: '編集', onClick: handleEdit },
    { icon: <IconTrash size="16" />, label: '削除', onClick: handleDelete, danger: true },
  ]

  return (
    <div>
      <HStack>
        <HStack gap="4" className={style.comment}>
          <AvatarLink src={author.avatar} size="m" nickname={author.nickname} />
          <VStack gap="4" className="w_full">
            {!isEdit ? (
              <div>
                <div className={style.comment_info}>
                  <span className="mr_4">{author.nickname}</span>
                  <time>{formatDatetime(created)}</time>
                </div>
                <p className={style.text}>{text}</p>
              </div>
            ) : (
              <CommentUpdate value={commentText} onChange={handleComment} onSubmit={handleUpdate(id, commentText)} onCancel={handleEditToggle} />
            )}

            <HStack gap="4" className="fs_12">
              <CountLike isLike={isLike} disable={!isActive} like={totalLike} onClick={handleLike(id)} />
              <ReplyView isView={isReplyView} onClick={handleReplyView} />
              <ThreadView isView={isThreadView} count={replys.length || 0} onClick={handleThreadView} />
            </HStack>

            <ReplyInput author={author} value={replyText} open={isReplyView} onChange={handleReply} onSubmit={handleReplyInput(id, replyText)} onCancel={handleReplyCancel} />
          </VStack>
        </HStack>
        <CommentAction open={isMenu} onMenu={handleMenu} actionRef={actionButtonRef} disabled={disabled} actionItems={actionItems} />
        <CommentDeleteModal open={isModal} onClose={handleModal} onAction={() => {}} comment={comment} />
      </HStack>

      {isThreadView && (
        <VStack gap="5" className={clsx(replys.length > 0 && 'mt_10 ml_50')}>
          {replys.map((reply) => (
            <div key={reply.id}>
              <CommentThread reply={reply} isActive={isActive} disabled={reply.author.nickname !== nickname} />
            </div>
          ))}
        </VStack>
      )}
    </div>
  )
}
