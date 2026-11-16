import { MediaSeries, Video, Music, Blog, Comic, Picture } from 'types/internal/media/output'
import { MediaPath } from 'utils/constants/enum'
import VStack from 'components/parts/Stack/Vertical'
import Advertise from 'components/widgets/Advertise'
import style from './Common.module.scss'
import MediaDetailSeries from '../Series'
import MediaSideImage from '../Side/Image'
import MediaSideMusic from '../Side/Music'

type MediaItem = Video | Music | Blog | Comic | Picture

const isMusicMedia = (media: MediaItem): media is Music => 'music' in media

interface Props {
  ulid: string
  list: Video[] | Music[] | Blog[] | Comic[] | Picture[]
  series: MediaSeries<MediaItem>
  mediaPath: MediaPath
  userUlid: string
}

export default function MediaDetailRight(props: Props): React.JSX.Element {
  const { ulid, list, series, mediaPath, userUlid } = props

  return (
    <div className={style.media_detail_right}>
      <Advertise userUlid={userUlid} className={style.advertise} />
      <MediaDetailSeries series={series} ulid={ulid} mediaPath={mediaPath} className={style.series} />
      <VStack gap="4">
        {list.map((media) =>
          isMusicMedia(media) ? (
            <MediaSideMusic key={media.ulid} href={`/media/${mediaPath}/${media.ulid}`} item={media} />
          ) : (
            <MediaSideImage key={media.ulid} href={`/media/${mediaPath}/${media.ulid}`} src={media.image} media={media} />
          ),
        )}
      </VStack>
    </div>
  )
}
