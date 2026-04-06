import Link from 'next/link'
import { Picture } from 'types/internal/media'
import ExImage from 'components/parts/ExImage'
import MediaContent from 'components/widgets/Media/Content'
import style from './Picture.module.scss'

interface Props {
  data: Picture
}

export default function MediaPicture(props: Props): React.JSX.Element {
  const { data } = props
  const { ulid, image } = data

  return (
    <section className={style.media}>
      <Link href={`/media/picture/${ulid}`}>
        <ExImage src={image} width="270" height="153" className={style.thumbnail} />
      </Link>
      <MediaContent href={`/media/picture/${ulid}`} media={data} />
    </section>
  )
}
