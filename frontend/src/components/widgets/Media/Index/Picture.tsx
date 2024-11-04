import Link from 'next/link'
import { Picture } from 'types/internal/media'
import ExImage from 'components/parts/ExImage'
import MediaContent from 'components/widgets/Common/MediaContent'
import style from './Media.module.scss'

interface Props {
  media: Picture
}

export default function MediaPicture(props: Props) {
  const { media } = props
  const { id, image } = media

  return (
    <section className={style.media}>
      <div className={style.decolation}>
        <Link href={`/media/picture/${id}`}>
          <ExImage src={image} width="272" height="153" className={style.avatar} />
        </Link>
        <MediaContent href={`/media/picture/${id}`} media={media} />
      </div>
    </section>
  )
}
