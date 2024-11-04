import Link from 'next/link'
import { Picture } from 'types/internal/media'
import ExImage from 'components/parts/ExImage'
import MediaContent from 'components/widgets/Common/MediaContent'
import style from './Media.module.scss'

interface Props {
  data: Picture
}

export default function MediaBlog(props: Props) {
  const { data } = props
  const { id, title, image, read, like, created, author } = data

  return (
    <section className={style.media}>
      <div className={style.decolation}>
        <Link href={`/media/blog/${id}`}>
          <ExImage src={image} width="272" height="153" className={style.section_image} />
        </Link>
        <MediaContent href={`/media/blog/${id}`} title={title} read={read} totalLike={like} created={created} author={author} />
      </div>
    </section>
  )
}
