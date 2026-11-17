import { Media } from 'types/internal/media/output'
import Card from 'components/parts/Card'
import ExImage from 'components/parts/ExImage'
import Link from 'components/parts/Link'
import style from './Image.module.scss'
import CardMediaContent from '../Content'

interface Props {
  href: string
  image: string
  media: Media
  badge?: string
}

export default function ImageCard(props: Props): React.JSX.Element {
  const { href, image, media, badge } = props

  return (
    <Card className={style.card}>
      <div className={style.thumbnail_box}>
        <Link href={href}>
          <ExImage src={image} width="312" height="195" className={style.thumbnail} />
        </Link>
        {badge && <span className={style.badge}>{badge}</span>}
      </div>
      <CardMediaContent href={href} media={media} />
    </Card>
  )
}
