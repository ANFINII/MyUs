import { Author } from 'types/internal/media'
import { formatDatetime } from 'utils/functions/datetime'
import style from './Info.module.scss'

export interface Props {
  comment: {
    author: Author
    created: Date
    text: string
  }
}

export default function CommentInfo(props: Props): React.JSX.Element {
  const { comment } = props
  const { author, created, text } = comment

  return (
    <div className={style.comment_info}>
      <div className={style.name}>
        <span className="mr_4">{author.nickname}</span>
        <time>{formatDatetime(created)}</time>
      </div>
      <p className={style.text}>{text}</p>
    </div>
  )
}
