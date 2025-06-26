import { useState } from 'react'
import { Comment } from 'types/internal/comment'
import { formatDatetime } from 'utils/functions/datetime'
import AvatarLink from 'components/parts/Avatar/Link'
import IconDots from 'components/parts/Icon/Dots'
import Horizontal from 'components/parts/Stack/Horizontal'
import CommentDeleteModal from 'components/widgets/Modal/CommentDelete'
import style from './CommentContent.module.scss'

export interface Props {
  comment: Comment
  nickname?: string
}

export default function CommentContent(props: Props): JSX.Element {
  const { comment, nickname } = props
  const { author, created, text } = comment

  const [isOpen, setIsOpen] = useState<boolean>(false)

  const handleModal = () => setIsOpen(!isOpen)

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
          <>
            <button className={style.edit_button} onClick={handleModal}>
              <IconDots size="18" />
            </button>
            {/* <div className={style.edit_button}>
              <span className={style.edit_button_update}>編集</span>
              <span className={style.edit_button_delete} onClick={handleModal}>
                削除
              </span>
            </div> */}
          </>
        )}
      </Horizontal>
      <CommentDeleteModal open={isOpen} onClose={handleModal} onAction={() => {}} comment={comment} />
    </>
  )
}
