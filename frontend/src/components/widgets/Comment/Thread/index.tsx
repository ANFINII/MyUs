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
  const { isActive, ulid } = user

  const actionButtonRef = useRef<HTMLButtonElement>(null)
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isMenu, setIsMenu] = useState<boolean>(false)
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const [isModal, setIsModal] = useState<boolean>(false)
  const [isLike, setIsLike] = useState<boolean>(isCommentLike || false)
  const [commentText, setCommentText] = useState<string>('')

  const disabled = author.ulid !== ulid
  const handleMenu = () => setIsMenu(!isMenu)
  const handleModal = () => setIsModal(!isModal)
  const handleEditToggle = () => setIsEdit(!isEdit)
  const handleComment = (e: ChangeEvent<HTMLTextAreaElement>) => setCommentText(e.target.value)

  const handleLike = async () => {
    if (isLike) {
      const ret = await deleteCommentLike(id)
      if (ret.isErr()) return
    } else {
      const ret = await postCommentLike(id)
      if (ret.isErr()) return
    }
    setIsLike(!isLike)
  }

  const handleEdit = () => {
    if (!isEdit) setCommentText(text)
    handleEditToggle()
  }

  const handleUpdate = async () => {
    setIsLoading(true)
    const text = commentText
    const ret = await putComment(id, { text })
    if (ret.isErr()) {
      handleToast(FetchError.Put, true)
      setIsLoading(false)
      return
    }
    setReplys((prev) => prev.map((comment) => (comment.id === id ? { ...comment, text } : comment)))
    setIsLoading(false)
    handleEditToggle()
  }

  const handleReplyDelete = async () => {
    setIsLoading(true)
    const ret = await deleteComment(id)
    if (ret.isErr()) {
      setIsLoading(false)
      handleToast(FetchError.Delete, true)
      return
    }
    setReplys((prev) => prev.filter((comment) => comment.id !== id))
    setIsLoading(false)
    handleModal()
  }

  const actionItems = [
    { icon: <IconEdit size="16" />, label: '編集', onClick: handleEdit },
    { icon: <IconTrash size="16" />, label: '削除', onClick: handleModal, danger: true },
  ]

  return (
    <HStack gap="4" className={style.reply}>
      <AvatarLink src={author.avatar} size="s" ulid={author.ulid} nickname={author.nickname} />
      <VStack gap="4" className="w_full">
        {!isEdit ? <CommentInfo comment={reply} /> : <CommentUpdate value={commentText} onChange={handleComment} onSubmit={handleUpdate} onCancel={handleEditToggle} />}
        <div className="fs_12">
          <CountLike isLike={isLike} disable={!isActive} like={totalLike} onClick={handleLike} />
        </div>
      </VStack>
      <CommentAction open={isMenu} onMenu={handleMenu} actionRef={actionButtonRef} disabled={disabled} actionItems={actionItems} />
      <CommentDeleteModal open={isModal} onClose={handleModal} onAction={handleReplyDelete} loading={isLoading} comment={reply} />
    </HStack>
  )
}
