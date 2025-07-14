import { useState, useRef, SetStateAction } from 'react'
import router from 'next/router'
import clsx from 'clsx'
import { capitalize } from 'lodash'
import { UserMe } from 'types/internal/auth'
import { Comment, CommnetIn, Reply } from 'types/internal/comment'
import { deleteComment, deleteCommentLike, postComment, postCommentLike, putComment } from 'api/internal/media/detail'
import { CommentType, FetchError } from 'utils/constants/enum'
import { commentTypeNoMap } from 'utils/constants/map'
import AvatarLink from 'components/parts/Avatar/Link'
import CountLike from 'components/parts/Count/Like'
import IconEdit from 'components/parts/Icon/Edit'
import IconTrash from 'components/parts/Icon/Trash'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
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
  setComments: (value: SetStateAction<Comment[]>) => void
  handleToast: (content: string, isError: boolean) => void
}

export default function CommentContent(props: Props): JSX.Element {
  const { comment, user, setComments, handleToast } = props
  const { id, author, text, isCommentLike, totalLike } = comment
  const { isActive, nickname } = user

  const actionButtonRef = useRef<HTMLButtonElement>(null)
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isMenu, setIsMenu] = useState<boolean>(false)
  const [isModal, setIsModal] = useState<boolean>(false)
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const [isReplyView, setIsReplyView] = useState<boolean>(false)
  const [isThreadView, setIsThreadView] = useState<boolean>(false)
  const [isLike, setIsLike] = useState<boolean>(isCommentLike || false)
  const [commentText, setCommentText] = useState<string>('')
  const [replyText, setReplyText] = useState<string>('')
  const [replys, setReplys] = useState<Reply[]>(comment.replys)

  const disabled = author.nickname !== nickname
  const handleMenu = () => setIsMenu(!isMenu)
  const handleModal = () => setIsModal(!isModal)
  const handleDelete = () => setIsModal(!isModal)
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

  const handleMediaReply = (parentId: number, text: string) => async () => {
    setIsLoading(true)
    const typeName = capitalize(String(router.pathname.split('/')[2]))
    const typeNo = commentTypeNoMap[typeName as CommentType]
    const objectId = Number(router.query.id)
    const request: CommnetIn = { text, typeNo, typeName, objectId, parentId }
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

  const handleUpdate = (commentId: number, text: string) => async () => {
    setIsLoading(true)
    const ret = await putComment(commentId, { text })
    if (ret.isErr()) {
      handleToast(FetchError.Put, true)
      setIsLoading(false)
      return
    }
    setComments((prev) => prev.map((comment) => (comment.id === commentId ? { ...comment, text } : comment)))
    setIsLoading(false)
    handleEditToggle()
  }

  const handleCommentDelete = (commentId: number) => async () => {
    setIsLoading(true)
    const ret = await deleteComment(commentId)
    if (ret.isErr()) {
      setIsLoading(false)
      handleToast(FetchError.Delete, true)
      return
    }
    setComments((prev) => prev.filter((comment) => comment.id !== commentId))
    handleModal()
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
        <HStack gap="4" className="w_full">
          <AvatarLink src={author.avatar} nickname={author.nickname} />
          <VStack gap="4" className="w_full">
            {!isEdit ? (
              <CommentInfo comment={comment} />
            ) : (
              <CommentUpdate value={commentText} onChange={handleComment} onSubmit={handleUpdate(id, commentText)} onCancel={handleEditToggle} />
            )}
            <HStack gap="4" className="fs_12">
              <CountLike isLike={isLike} disable={!isActive} like={totalLike} onClick={handleLike(id)} />
              <View isView={isReplyView} onView={handleReplyView} size="s" color="grey" content="返信" />
              <View isView={isThreadView} onView={handleThreadView} size="s" color="grey" content={`スレッド ${replys.length || 0} 件`} />
            </HStack>
            <ReplyInput user={user} value={replyText} open={isReplyView} onChange={handleReply} onSubmit={handleMediaReply(id, replyText)} onCancel={handleReplyCancel} />
          </VStack>
        </HStack>
        <CommentAction open={isMenu} onMenu={handleMenu} actionRef={actionButtonRef} disabled={disabled} actionItems={actionItems} />
        <CommentDeleteModal open={isModal} onClose={handleModal} loading={isLoading} onAction={handleCommentDelete(id)} comment={comment} />
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
