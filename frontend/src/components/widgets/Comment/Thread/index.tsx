import { ChangeEvent, SetStateAction, useRef, useState } from 'react'
import { UserMe } from 'types/internal/auth'
import { Reply } from 'types/internal/comment'
import { postCommentLike, putComment, deleteComment, deleteCommentLike } from 'api/internal/media/comment'
import { FetchError } from 'utils/constants/enum'
import AvatarLink from 'components/parts/Avatar/Link'
import CountLike from 'components/parts/Count/Like'
import IconEdit from 'components/parts/Icon/Edit'
import IconTrash from 'components/parts/Icon/Trash'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import CommentDeleteModal from 'components/widgets/Modal/CommentDelete'
import CommentAction from '../Action'
import CommentUpdate from '../Update'
import style from './Thread.module.scss'
import CommentInfo from '../Info'

interface Props {
  reply: Reply
  user: UserMe
  setReplys: (value: SetStateAction<Reply[]>) => void
  handleToast: (content: string, isError: boolean) => void
}

export default function CommentThread(props: Props): JSX.Element {
  const { reply, user, setReplys, handleToast } = props
  const { id, author, text, isCommentLike, totalLike } = reply
  const { isActive, nickname } = user

  const actionButtonRef = useRef<HTMLButtonElement>(null)
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isMenu, setIsMenu] = useState<boolean>(false)
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const [isModal, setIsModal] = useState<boolean>(false)
  const [isLike, setIsLike] = useState<boolean>(isCommentLike || false)
  const [commentText, setCommentText] = useState<string>('')

  const disabled = author.nickname !== nickname
  const handleMenu = () => setIsMenu(!isMenu)
  const handleModal = () => setIsModal(!isModal)
  const handleEditToggle = () => setIsEdit(!isEdit)
  const handleComment = (e: ChangeEvent<HTMLTextAreaElement>): void => setCommentText(e.target.value)

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

  const handleUpdate = (commentId: number, text: string) => async () => {
    setIsLoading(true)
    const ret = await putComment(commentId, { text })
    if (ret.isErr()) {
      handleToast(FetchError.Put, true)
      setIsLoading(false)
      return
    }
    setReplys((prev) => prev.map((comment) => (comment.id === commentId ? { ...comment, text } : comment)))
    setIsLoading(false)
    handleEditToggle()
  }

  const handleReplyDelete = (commentId: number) => async () => {
    setIsLoading(true)
    const ret = await deleteComment(commentId)
    if (ret.isErr()) {
      setIsLoading(false)
      handleToast(FetchError.Delete, true)
      return
    }
    setReplys((prev) => prev.filter((comment) => comment.id !== commentId))
    setIsLoading(false)
    handleModal()
  }

  const actionItems = [
    { icon: <IconEdit size="16" />, label: '編集', onClick: handleEdit },
    { icon: <IconTrash size="16" />, label: '削除', onClick: handleModal, danger: true },
  ]

  return (
    <HStack gap="4" className={style.reply}>
      <AvatarLink src={author.avatar} size="s" nickname={author.nickname} />
      <VStack gap="4" className="w_full">
        {!isEdit ? (
          <CommentInfo comment={reply} />
        ) : (
          <CommentUpdate value={commentText} onChange={handleComment} onSubmit={handleUpdate(id, commentText)} onCancel={handleEditToggle} />
        )}
        <div className="fs_12">
          <CountLike isLike={isLike} disable={!isActive} like={totalLike} onClick={handleLike(id)} />
        </div>
      </VStack>
      <CommentAction open={isMenu} onMenu={handleMenu} actionRef={actionButtonRef} disabled={disabled} actionItems={actionItems} />
      <CommentDeleteModal open={isModal} onClose={handleModal} onAction={handleReplyDelete(id)} loading={isLoading} comment={reply} />
    </HStack>
  )
}
