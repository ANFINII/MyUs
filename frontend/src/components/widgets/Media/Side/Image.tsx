import Link from 'next/link'
import { Media } from 'types/internal/media'
import ExImage from 'components/parts/ExImage'
import Horizontal from 'components/parts/Stack/Horizontal'
import MediaBaseContent from 'components/widgets/Media/Content/Base'
import style from './Side.module.scss'

interface Props {
  href: string
  src: string
  media: Media
}

export default function MediaSideImage(props: Props): JSX.Element {
  const { href, src, media } = props

  return (
    <section>
      <Link href={href} className={style.link}>
        <Horizontal gap="4">
          <ExImage src={src} width="192" height="100" className={style.thumbnail} />
          <MediaBaseContent media={media} />
        </Horizontal>
      </Link>
    </section>
  )
}
