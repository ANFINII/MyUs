import Link from 'next/link'
import { Comic } from 'types/internal/media'
import ExImage from 'components/parts/ExImage'
import style from './Comic.module.scss'
import CardMediaContent from '../Media/Content'

interface Props {
  item: Comic
}

export default function ComicCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, image } = item

  return (
    <section className={style.card}>
      <Link href={`/media/comic/${ulid}`}>
        <ExImage src={image} width="270" height="153" className={style.thumbnail} />
      </Link>
      <CardMediaContent href={`/media/comic/${ulid}`} media={item} />
    </section>
  )
}
