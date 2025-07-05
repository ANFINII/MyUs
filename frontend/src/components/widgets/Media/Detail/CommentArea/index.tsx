import clsx from 'clsx'
import { Comment } from 'types/internal/comment'
import { useUser } from 'components/hooks/useUser'
import VStack from 'components/parts/Stack/Vertical'
import CommentContent from 'components/widgets/Comment/Content'
import style from './CommentArea.module.scss'

interface Props {
  comments: Comment[]
  onLikeComment: (commentId: number) => void
  isView: boolean
  nickname?: string
}

export default function CommentArea(props: Props): JSX.Element {
  const { comments, onLikeComment, isView, nickname } = props
  const { user } = useUser()

  return (
    <VStack gap="10" className={clsx(style.comment_aria, isView && style.active)}>
      {comments.map((comment) => {
        const disabled = comment.author.nickname !== nickname
        return (
          <div key={comment.id}>
            <CommentContent comment={comment} disabled={disabled} isActive={user.isActive} onLikeComment={onLikeComment} />
          </div>
        )
      })}
    </VStack>
  )
}
