import { Channel } from 'types/internal/channel'
import { Comment } from 'types/internal/comment'
import { MediaUser, Video, Music, Picture, Blog } from 'types/internal/media'
import { Hashtag } from 'types/internal/media/detail'
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
