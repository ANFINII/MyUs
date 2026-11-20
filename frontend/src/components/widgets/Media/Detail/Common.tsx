import { Channel } from 'types/internal/channel'
import { Comment } from 'types/internal/comment'
import { Hashtag, MediaSeries, MediaUser, Video, Audio, Blog, Comic, Picture } from 'types/internal/media/output'
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
  list: Video[] | Audio[] | Blog[] | Picture[]
  series: MediaSeries<Video | Audio | Blog | Comic | Picture>
  handleToast: (content: string, isError: boolean) => void
}

export default function MediaDetailCommon(props: Props): React.JSX.Element {
  const { media, list, series, handleToast } = props

  return (
    <div className={style.media_detail}>
      <MediaDetailLeft key={media.ulid} media={media} handleToast={handleToast} />
      <MediaDetailRight ulid={media.ulid} list={list} series={series} mediaPath={media.mediaPath} userUlid={media.channel.ownerUlid} />
    </div>
  )
}
