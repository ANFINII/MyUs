import { ChangeEvent, Dispatch, SetStateAction, useRef, useState } from 'react'
import { LikeCommentIn, UserMe } from 'types/internal/auth'
import { Reply } from 'types/internal/comment'
import { putComment, deleteComment } from 'api/internal/media/comment'
import { postLikeComment } from 'api/internal/user'
import { FetchError } from 'utils/constants/enum'
import { useIsLoading } from 'components/hooks/useIsLoading'
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
import { CommentContentState } from '../Content'
import CommentInfo from '../Info'

export interface CommentThreadState {
  isLike: boolean
  likeCount: number
  commentText: string
}

interface Props {
  reply: Reply
  user: UserMe
  setParentState: Dispatch<SetStateAction<CommentContentState>>
  handleToast: (content: string, isError: boolean) => void
}

export default function CommentThread(props: Props): JSX.Element {
  const { reply, user, setParentState, handleToast } = props
  const { id, author, text } = reply
  const { isActive, ulid } = user

  const initFormState: CommentThreadState = {
    isLike: reply.isCommentLike,
    likeCount: reply.likeCount,
    commentText: '',
  }

  const actionButtonRef = useRef<HTMLButtonElement>(null)
  const { isLoading, handleLoading } = useIsLoading()
  const [isMenu, setIsMenu] = useState<boolean>(false)
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const [isModal, setIsModal] = useState<boolean>(false)
  const [formState, setFormState] = useState<CommentThreadState>(initFormState)

  const { isLike, likeCount, commentText } = formState
  const disabled = author.ulid !== ulid
  const handleMenu = () => setIsMenu(!isMenu)
  const handleModal = () => setIsModal(!isModal)
  const handleEditToggle = () => setIsEdit(!isEdit)
  const handleComment = (e: ChangeEvent<HTMLTextAreaElement>) => setFormState((prev) => ({ ...prev, commentText: e.target.value }))

  const handleLike = async () => {
    const request: LikeCommentIn = { id, isLike: !isLike }
    const ret = await postLikeComment(request)
    if (ret.isErr()) return handleToast(FetchError.Post, true)
    const data = ret.value
    setFormState((prev) => ({ ...prev, ...data }))
  }

  const handleEdit = () => {
    setFormState((prev) => ({ ...prev, commentText: text }))
    handleEditToggle()
  }

  const handleUpdate = async () => {
    handleLoading(true)
    const text = commentText
    const ret = await putComment(id, { text })
    if (ret.isErr()) {
      handleToast(FetchError.Put, true)
      handleLoading(false)
      return
    }
    setParentState((prev) => ({ ...prev, replys: prev.replys.map((c) => (c.id === id ? { ...c, text } : c)) }))
    handleLoading(false)
    handleEditToggle()
  }

  const handleDelete = async () => {
    handleLoading(true)
    const ret = await deleteComment(id)
    if (ret.isErr()) {
      handleLoading(false)
      handleToast(FetchError.Delete, true)
      return
    }
    setParentState((prev) => ({ ...prev, replys: prev.replys.filter((c) => c.id !== id) }))
    handleLoading(false)
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
          <CountLike isLike={isLike} disable={!isActive} count={likeCount} onClick={handleLike} />
        </div>
      </VStack>
      <CommentAction open={isMenu} onMenu={handleMenu} actionRef={actionButtonRef} disabled={disabled} actionItems={actionItems} />
      <CommentDeleteModal open={isModal} onClose={handleModal} onAction={handleDelete} loading={isLoading} comment={reply} />
    </HStack>
  )
}
