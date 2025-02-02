import Link from 'next/link'
import { Blog } from 'types/internal/media'
import ExImage from 'components/parts/ExImage'
import MediaContent from 'components/widgets/Media/Content'
import style from './Media.module.scss'

interface Props {
  media: Blog
}

export default function MediaBlog(props: Props): JSX.Element {
  const { media } = props
  const { id, image } = media

  return (
    <section className={style.media}>
      <Link href={`/media/blog/${id}`}>
        <ExImage src={image} width="270" height="153" className={style.thumbnail} />
      </Link>
      <MediaContent href={`/media/blog/${id}`} media={media} />
    </section>
  )
}
