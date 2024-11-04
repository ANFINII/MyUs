import Link from 'next/link'
import { Picture } from 'types/internal/media'
import ExImage from 'components/parts/ExImage'
import MediaContent from 'components/widgets/Common/MediaContent'
import style from './Media.module.scss'

interface Props {
  data: Picture
}

export default function MediaPicture(props: Props) {
  const { data } = props
  const { author, id, title, image, read, like, created } = data

  return (
    <section className={style.section_list}>
      <div className={style.decolation}>
        <Link href={`/media/picture/${id}`}>
          <ExImage src={image} width="272" height="153" className={style.section_image} />
          <MediaContent author={author} title={title} read={read} totalLike={like} created={created} />
        </Link>
      </div>
    </section>
  )
}
