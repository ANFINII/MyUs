import { Audio } from 'types/internal/media/output'
import ExImage from 'components/parts/ExImage'
import Link from 'components/parts/Link'
import HStack from 'components/parts/Stack/Horizontal'
import CardMediaContentBase from 'components/widgets/Card/Media/Content/Base'
import style from './Side.module.scss'

interface Props {
  href: string
  item: Audio
}

export default function MediaSideAudio(props: Props): React.JSX.Element {
  const { href, item } = props
  const { image, channel } = item

  return (
    <section>
      <Link href={href} className={style.link}>
        <HStack gap="4">
          <div className={style.thumbnail_box}>
            <ExImage src={image || channel.avatar} width="100" height="100" className={style.square} />
          </div>
          <CardMediaContentBase media={item} />
        </HStack>
      </Link>
    </section>
  )
}
