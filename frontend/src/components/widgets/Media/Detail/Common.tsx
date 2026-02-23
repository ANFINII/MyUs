import { Channel } from 'types/internal/channle'
import { Comment } from 'types/internal/comment'
import { MediaUser, Video, Music, Picture, Blog } from 'types/internal/media'
import style from './Common.module.scss'
import MediaDetailLeft from './Left'
import MediaDetailRight from './Right'

interface Props {
  media: {
    title: string
    content: string
    read: number
    like: number
    created: Date
    comments: Comment[]
    channel: Channel
    mediaUser: MediaUser
    type: 'video' | 'music' | 'comic' | 'picture' | 'blog'
  }
  list: Video[] | Music[] | Picture[] | Blog[]
  isAd?: boolean
  handleToast: (content: string, isError: boolean) => void
}

export default function MediaDetailCommon(props: Props): React.JSX.Element {
  const { media, list, isAd, handleToast } = props

  return (
    <div className={style.media_detail}>
      <MediaDetailLeft media={media} handleToast={handleToast} />
      <MediaDetailRight isAd={isAd} list={list} />
    </div>
  )
}
