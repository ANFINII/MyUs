import { Video, Music, Blog, Picture, Comic } from 'types/internal/media'
import { MediaPath } from 'utils/constants/enum'
import Divide from 'components/parts/Divide'
import VStack from 'components/parts/Stack/Vertical'
import Advertise from 'components/widgets/Advertise'
import MusicCard from 'components/widgets/Card/Music'
import style from './Common.module.scss'
import MediaSideImage from '../Side/Image'

type MediaItem = Video | Music | Comic | Picture | Blog

const isMusicMedia = (media: MediaItem): media is Music => 'music' in media

interface Props {
  list: Video[] | Music[] | Comic[] | Picture[] | Blog[]
  mediaPath: MediaPath
  isAd?: boolean
  isChannelAd?: boolean
}

export default function MediaDetailRight(props: Props): React.JSX.Element {
  const { list, mediaPath, isAd = false, isChannelAd = false } = props

  return (
    <div className={style.media_detail_right}>
      {isAd && <Advertise isChannelAd={isChannelAd} className={style.advertise} />}
      {isAd && <Divide />}
      <VStack gap="4">
        {list.map((media) =>
          isMusicMedia(media) ? (
            <MusicCard key={media.ulid} item={media} />
          ) : (
            <MediaSideImage key={media.ulid} href={`/media/${mediaPath}/${media.ulid}`} src={media.image} media={media} />
          ),
        )}
      </VStack>
    </div>
  )
}
