import { Music } from 'types/internal/media/output'
import cx from 'utils/functions/cx'
import { useMusicPlayer } from 'components/hooks/useMusicPlayer'
import ExImage from 'components/parts/ExImage'
import Link from 'components/parts/Link'
import HStack from 'components/parts/Stack/Horizontal'
import CardMediaContentBase from 'components/widgets/Card/Media/Content/Base'
import style from './Side.module.scss'

interface Props {
  href: string
  item: Music
  items: Music[]
}

export default function MediaSideMusic(props: Props): React.JSX.Element {
  const { href, item, items } = props
  const { ulid, image, channel } = item

  const { current, play, toggle } = useMusicPlayer()

  const isCurrent = current?.ulid === ulid

  const handlePlay = () => (isCurrent ? toggle() : play(items, Math.max(items.findIndex((m) => m.ulid === ulid), 0)))

  return (
    <section>
      <HStack gap="4">
        <div className={cx(style.music_thumbnail_wrap, isCurrent && style.current)} onClick={handlePlay}>
          <ExImage src={image || channel.avatar} width="100" height="100" className={style.music_thumbnail} />
          <span className={style.play} />
        </div>
        <Link href={href} className={style.link}>
          <CardMediaContentBase media={item} />
        </Link>
      </HStack>
    </section>
  )
}
