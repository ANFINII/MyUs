import { Comment } from 'types/internal/comment'
import { Author, Blog, MediaUser, Video } from 'types/internal/media'
import style from './Common.module.scss'
import MediaDetailLeft from './Left'
import MediaDetailRight from './Right'

interface Props {
  media: {
    title: string
    content: string
    read: number
    likeCount: number
    created: Date
    comments: Comment[]
    author: Author
    mediaUser: MediaUser
    type: 'video' | 'music' | 'comic' | 'picture' | 'blog'
  }
  list: Video[] | Blog[]
  handleToast: (content: string, isError: boolean) => void
}

export default function MediaDetailCommon(props: Props): React.JSX.Element {
  const { media, list, handleToast } = props

  return (
    <div className={style.media_detail}>
      <MediaDetailLeft media={media} handleToast={handleToast} />
      <MediaDetailRight list={list} />
    </div>
  )
}
