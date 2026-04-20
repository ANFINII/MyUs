import { Channel } from 'types/internal/channel'
import { Comment } from 'types/internal/comment'
import { MediaUser, Video, Music, Blog, Picture } from 'types/internal/media/output'
import { Hashtag } from 'types/internal/media/output'
import { MediaPath } from 'utils/constants/enum'
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
    hashtags: Hashtag[]
    channel: Channel
    mediaUser: MediaUser
    mediaPath: MediaPath
  }
  list: Video[] | Music[] | Blog[] | Picture[]
  isAd?: boolean
  handleToast: (content: string, isError: boolean) => void
}

export default function MediaDetailCommon(props: Props): React.JSX.Element {
  const { media, list, isAd, handleToast } = props

  return (
    <div className={style.media_detail}>
      <MediaDetailLeft media={media} handleToast={handleToast} />
      <MediaDetailRight list={list} mediaPath={media.mediaPath} isAd={isAd} />
    </div>
  )
}
