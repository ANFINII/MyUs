import Link from 'next/link'
import { Blog } from 'types/internal/media'
import ExImage from 'components/parts/ExImage'
import MediaContent from 'components/widgets/Media/Content'
import style from './Blog.module.scss'

interface Props {
  data: Blog
}

export default function MediaBlog(props: Props): React.JSX.Element {
  const { data } = props
  const { ulid, image } = data

  return (
    <section className={style.media}>
      <Link href={`/media/blog/${ulid}`}>
        <ExImage src={image} width="270" height="153" className={style.thumbnail} />
      </Link>
      <MediaContent href={`/media/blog/${ulid}`} media={data} />
    </section>
  )
}
