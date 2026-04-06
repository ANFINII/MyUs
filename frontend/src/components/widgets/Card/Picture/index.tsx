import Link from 'next/link'
import { Picture } from 'types/internal/media'
import ExImage from 'components/parts/ExImage'
import style from './Picture.module.scss'
import CardMediaContent from '../Media/Content'

interface Props {
  item: Picture
}

export default function PictureCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, image } = item

  return (
    <section className={style.card}>
      <Link href={`/media/picture/${ulid}`}>
        <ExImage src={image} width="270" height="153" className={style.thumbnail} />
      </Link>
      <CardMediaContent href={`/media/picture/${ulid}`} media={item} />
    </section>
  )
}
