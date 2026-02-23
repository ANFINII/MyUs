import { Video, Music, Blog, Picture } from 'types/internal/media'
import Divide from 'components/parts/Divide'
import VStack from 'components/parts/Stack/Vertical'
import Advertise from 'components/widgets/Advertise'
import MediaMusic from 'components/widgets/Media/Index/Music'
import style from './Common.module.scss'
import MediaSideImage from '../Side/Image'

type MediaItem = Video | Music | Picture | Blog

const isMusicMedia = (media: MediaItem): media is Music => 'music' in media

interface Props {
  list: Video[] | Music[] | Picture[] | Blog[]
  isAd?: boolean
  isChannelAd?: boolean
}

export default function MediaDetailRight(props: Props): React.JSX.Element {
  const { list, isAd = false, isChannelAd = false } = props

  return (
    <div className={style.media_detail_right}>
      {isAd && <Advertise isChannelAd={isChannelAd} className={style.advertise} />}
      {isAd && <Divide />}
      <VStack gap="4">
        {list.map((media) =>
          isMusicMedia(media) ? (
            <MediaMusic key={media.ulid} media={media} />
          ) : (
            <MediaSideImage key={media.ulid} href={`/media/blog/${media.ulid}`} src={media.image} media={media} />
          ),
        )}
      </VStack>
    </div>
  )
}
