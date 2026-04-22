import Link from 'next/link'
import { Comic } from 'types/internal/media/output'
import Card from 'components/parts/Card'
import ExImage from 'components/parts/ExImage'
import style from './Comic.module.scss'
import CardMediaContent from '../Content'

interface Props {
  item: Comic
}

export default function ComicCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, image } = item

  return (
    <Card className={style.card}>
      <Link href={`/media/comic/${ulid}`}>
        <ExImage src={image} width="312" height="195" className={style.thumbnail} />
      </Link>
      <CardMediaContent href={`/media/comic/${ulid}`} media={item} />
    </Card>
  )
}
