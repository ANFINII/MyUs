import Link from 'next/link'
import { Blog } from 'types/internal/media'
import ExImage from 'components/parts/ExImage'
import style from './Blog.module.scss'
import CardMediaContent from '../Media/Content'

interface Props {
  item: Blog
}

export default function BlogCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, image } = item

  return (
    <section className={style.card}>
      <Link href={`/media/blog/${ulid}`}>
        <ExImage src={image} width="270" height="153" className={style.thumbnail} />
      </Link>
      <CardMediaContent href={`/media/blog/${ulid}`} media={item} />
    </section>
  )
}
