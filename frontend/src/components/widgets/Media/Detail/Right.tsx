import { Video, Music, Blog, Comic, Picture } from 'types/internal/media/output'
import { MediaPath } from 'utils/constants/enum'
import VStack from 'components/parts/Stack/Vertical'
import Advertise from 'components/widgets/Advertise'
import style from './Common.module.scss'
import MediaSideImage from '../Side/Image'

interface Props {
  list: Video[] | Music[] | Blog[] | Comic[] | Picture[]
  mediaPath: MediaPath
  userUlid: string
}

export default function MediaDetailRight(props: Props): React.JSX.Element {
  const { list, mediaPath, userUlid } = props

  return (
    <div className={style.media_detail_right}>
      <Advertise userUlid={userUlid} className={style.advertise} />
      <VStack gap="4">
        {list.map((media) => (
          <MediaSideImage key={media.ulid} href={`/media/${mediaPath}/${media.ulid}`} src={media.image || media.channel.avatar} media={media} />
        ))}
      </VStack>
    </div>
  )
}
