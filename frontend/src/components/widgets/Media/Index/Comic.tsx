import Link from 'next/link'
import { Comic } from 'types/internal/media'
import ExImage from 'components/parts/ExImage'
import MediaContent from 'components/widgets/Common/MediaContent'
import style from './Media.module.scss'

interface Props {
  data: Comic
}

export default function MediaComic(props: Props) {
  const { data } = props
  const { author, id, title, image, read, like, created } = data

  return (
    <section className={style.section_list}>
      <div className={style.decolation}>
        <Link href={`/media/comic/${id}`}>
          <ExImage src={image} width="272" height="153" className="radius_8" />
          <MediaContent author={author} title={title} read={read} totalLike={like} created={created} />
        </Link>
      </div>
    </section>
  )
}
