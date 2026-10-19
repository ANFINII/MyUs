import { Channel } from 'types/internal/channel'
import { Comment } from 'types/internal/comment'
import { Hashtag, MediaUser, Video, Music, Blog, Picture } from 'types/internal/media/output'
import { MediaPath } from 'utils/constants/enum'
import style from './Common.module.scss'
import MediaDetailLeft from './Left'
import MediaDetailRight from './Right'

interface Props {
  media: {
    ulid: string
    title: string
    content: string
    read: number
    like: number
    created: Date
    comments: Comment[]
    hashtags: Hashtag[]
    channel: Channel
    mediaUser: MediaUser
    mediaPath: MediaPath
  }
  list: Video[] | Music[] | Blog[] | Picture[]
  handleToast: (content: string, isError: boolean) => void
}

export default function MediaDetailCommon(props: Props): React.JSX.Element {
  const { media, list, handleToast } = props

  return (
    <div className={style.media_detail}>
      <MediaDetailLeft key={media.ulid} media={media} handleToast={handleToast} />
      <MediaDetailRight list={list} mediaPath={media.mediaPath} userUlid={media.channel.ownerUlid} />
    </div>
  )
}
