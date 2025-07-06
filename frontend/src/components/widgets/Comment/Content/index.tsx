import { useState, useRef } from 'react'
import { Comment } from 'types/internal/comment'
import { deleteCommentLike, postCommentLike } from 'api/internal/media/detail'
import { formatDatetime } from 'utils/functions/datetime'
import AvatarLink from 'components/parts/Avatar/Link'
import Button from 'components/parts/Button'
import CountLike from 'components/parts/Count/Like'
import IconEdit from 'components/parts/Icon/Edit'
import IconTrash from 'components/parts/Icon/Trash'
import TextareaLine from 'components/parts/Input/Textarea/Line'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import CommentDeleteModal from 'components/widgets/Modal/CommentDelete'
import style from './CommentContent.module.scss'
import CommentAction from '../Action'
import ReplyInput from '../Reply/Input'
import ReplyView from '../Reply/View'
import CommentThread from '../Thread'

export interface Props {
  comment: Comment
  disabled: boolean
  isActive: boolean
}

export default function CommentContent(props: Props): JSX.Element {
  const { comment, disabled, isActive } = props
  const { author, created, text } = comment

  const actionButtonRef = useRef<HTMLButtonElement>(null)
  const [isMenu, setIsMenu] = useState<boolean>(false)
  const [isModal, setIsModal] = useState<boolean>(false)
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const [isReplyView, setIsReplyView] = useState<boolean>(false)
  const [isThreadView, setIsThreadView] = useState<boolean>(false)
  const [isLike, setIsLike] = useState<boolean>(comment.isCommentLike || false)
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

  const handleLike = async (commentId: number): Promise<void> => {
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

  const handleCommentUpdate = (commentId: number, text: string) => () => {
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
    <HStack>
      <HStack gap="4" className={style.comment}>
        <AvatarLink src={author.avatar} size="40" nickname={author.nickname} />
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
            <VStack gap="4">
              <TextareaLine name="text" placeholder="コメント入力" value={commentText} onChange={handleComment} className={style.textarea} />
              <HStack gap="4" justify="end">
                <Button size="s" name="キャンセル" onClick={handleEditToggle} />
                <Button size="s" color="green" name="更新" disabled={commentText.trim() === ''} onClick={handleCommentUpdate(comment.id, commentText)} />
              </HStack>
            </VStack>
          )}

          <HStack gap="4" className="fs_12">
            <CountLike isLike={isLike} disable={!isActive} like={comment.totalLike} onClick={() => handleLike(comment.id)} />
            <ReplyView isView={isReplyView} onClick={handleReplyView} />
            <CommentThread isView={isThreadView} count={comment.replyCount || 0} onClick={handleThreadView} />
          </HStack>

          <ReplyInput author={author} value={replyText} open={isReplyView} onChange={handleReply} onSubmit={handleReplyInput(comment.id, replyText)} onCancel={handleReplyCancel} />

          <div className={style.comment_aria_list_5} />
        </VStack>
      </HStack>
      <CommentAction open={isMenu} onMenu={handleMenu} actionRef={actionButtonRef} disabled={disabled} actionItems={actionItems} />
      <CommentDeleteModal open={isModal} onClose={handleModal} onAction={() => {}} comment={comment} />
    </HStack>
  )
}
