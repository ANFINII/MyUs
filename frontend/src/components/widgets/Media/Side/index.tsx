import Link from 'next/link'
import { Blog } from 'types/internal/media'
import ExImage from 'components/parts/ExImage'
import Horizontal from 'components/parts/Stack/Horizontal'
import MediaBaseContent from 'components/widgets/Media/Content/Base'
import style from './Side.module.scss'

interface Props {
  media: Blog
}

export default function MediaSideBlog(props: Props): JSX.Element {
  const { media } = props
  const { id, image } = media

  return (
    <section>
      <Link href={`/media/blog/${id}`} className={style.link}>
        <Horizontal gap="4">
          <ExImage src={image} width="192" height="100" className={style.thumbnail} />
          <MediaBaseContent media={media} />
        </Horizontal>
      </Link>
    </section>
  )
}
