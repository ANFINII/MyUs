import { useState, useRef, SetStateAction, ChangeEvent, Dispatch } from 'react'
import router from 'next/router'
import clsx from 'clsx'
import { capitalize } from 'lodash'
import { LikeCommentIn, UserMe } from 'types/internal/auth'
import { Reply, Comment, CommnetIn } from 'types/internal/comment'
import { postComment, putComment, deleteComment } from 'api/internal/media/comment'
import { postLikeComment } from 'api/internal/user'
import { CommentType, FetchError } from 'utils/constants/enum'
import { commentTypeNoMap } from 'utils/constants/map'
import AvatarLink from 'components/parts/Avatar/Link'
import CountLike from 'components/parts/Count/Like'
import IconEdit from 'components/parts/Icon/Edit'
import IconTrash from 'components/parts/Icon/Trash'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import { MediaDetailState } from 'components/widgets/Media/Detail/Common'
import CommentDeleteModal from 'components/widgets/Modal/CommentDelete'
import View from 'components/widgets/View'
import CommentAction from '../Action'
import CommentInfo from '../Info'
import ReplyInput from '../ReplyInput'
import CommentThread from '../Thread'
import CommentUpdate from '../Update'

export interface Props {
  comment: Comment
  user: UserMe
  setFormState: Dispatch<SetStateAction<MediaDetailState>>
  handleToast: (content: string, isError: boolean) => void
}

export default function CommentContent(props: Props): JSX.Element {
  const { comment, user, setFormState, handleToast } = props
  const { id, author, text, isCommentLike, likeCount } = comment
  const { isActive, ulid } = user

  const actionButtonRef = useRef<HTMLButtonElement>(null)
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isMenu, setIsMenu] = useState<boolean>(false)
  const [isModal, setIsModal] = useState<boolean>(false)
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const [isReplyView, setIsReplyView] = useState<boolean>(false)
  const [isThreadView, setIsThreadView] = useState<boolean>(false)
  const [isLike, setIsLike] = useState<boolean>(isCommentLike)
  const [commentText, setCommentText] = useState<string>('')
  const [replyText, setReplyText] = useState<string>('')
  const [replys, setReplys] = useState<Reply[]>(comment.replys)

  const disabled = author.ulid !== ulid
  const handleMenu = () => setIsMenu(!isMenu)
  const handleModal = () => setIsModal(!isModal)
  const handleEditToggle = () => setIsEdit(!isEdit)
  const handleReplyView = () => setIsReplyView(!isReplyView)
  const handleThreadView = () => setIsThreadView(!isThreadView)
  const handleComment = (e: ChangeEvent<HTMLTextAreaElement>) => setCommentText(e.target.value)
  const handleReply = (e: ChangeEvent<HTMLTextAreaElement>) => setReplyText(e.target.value)

  const handleLike = async () => {
    const request: LikeCommentIn = { id, isLike: !isLike }
    const ret = await postLikeComment(request)
    if (ret.isErr()) return handleToast(FetchError.Post, true)
    setIsLike(!isLike)
  }

  const handleEdit = () => {
    if (!isEdit) setCommentText(text)
    handleEditToggle()
  }

  const handleMediaReply = async () => {
    setIsLoading(true)
    const text = replyText
    const typeName = capitalize(String(router.pathname.split('/')[2]))
    const typeNo = commentTypeNoMap[typeName as CommentType]
    const objectId = Number(router.query.id)
    const parentId = id
    const request: CommnetIn = { text, typeName, typeNo, objectId, parentId }
    const ret = await postComment(request)
    if (ret.isErr()) {
      setIsLoading(false)
      handleToast(FetchError.Post, true)
      return
    }
    setReplys([ret.value, ...replys])
    setIsLoading(false)
    setReplyText('')
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
    setFormState((prev) => ({ ...prev, comments: prev.comments.map((c) => (c.id === id ? { ...c, text } : c)) }))
    setIsLoading(false)
    handleEditToggle()
  }

  const handleCommentDelete = async () => {
    setIsLoading(true)
    const ret = await deleteComment(id)
    if (ret.isErr()) {
      setIsLoading(false)
      handleToast(FetchError.Delete, true)
      return
    }
    setFormState((prev) => ({ ...prev, comments: prev.comments.filter((c) => c.id !== id) }))
    handleModal()
  }

  const handleReplyCancel = () => {
    setReplyText('')
    handleReplyView()
  }

  const actionItems = [
    { icon: <IconEdit size="16" />, label: '編集', onClick: handleEdit },
    { icon: <IconTrash size="16" />, label: '削除', onClick: handleModal, danger: true },
  ]

  return (
    <div>
      <HStack>
        <HStack gap="4" className="w_full">
          <AvatarLink src={author.avatar} ulid={author.ulid} nickname={author.nickname} />
          <VStack gap="4" className="w_full">
            {!isEdit ? <CommentInfo comment={comment} /> : <CommentUpdate value={commentText} onChange={handleComment} onSubmit={handleUpdate} onCancel={handleEditToggle} />}
            <HStack gap="4" className="fs_12">
              <CountLike isLike={isLike} disable={!isActive} count={likeCount} onClick={handleLike} />
              <View isView={isReplyView} onView={handleReplyView} size="s" color="grey" content="返信" />
              <View isView={isThreadView} onView={handleThreadView} size="s" color="grey" content={`スレッド ${replys.length || 0} 件`} />
            </HStack>
            <ReplyInput user={user} value={replyText} open={isReplyView} onChange={handleReply} onSubmit={handleMediaReply} onCancel={handleReplyCancel} />
          </VStack>
        </HStack>
        <CommentAction open={isMenu} onMenu={handleMenu} actionRef={actionButtonRef} disabled={disabled} actionItems={actionItems} />
        <CommentDeleteModal open={isModal} onClose={handleModal} loading={isLoading} onAction={handleCommentDelete} comment={comment} />
      </HStack>

      {isThreadView && (
        <VStack gap="5" className={clsx(replys.length > 0 && 'mt_10 ml_50')}>
          {replys.map((reply) => (
            <CommentThread key={reply.id} reply={reply} user={user} setReplys={setReplys} handleToast={handleToast} />
          ))}
        </VStack>
      )}
    </div>
  )
}
