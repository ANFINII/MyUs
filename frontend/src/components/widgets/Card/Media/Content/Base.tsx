import { Media } from 'types/internal/media/output'
import cx from 'utils/functions/cx'
import { useDatetime } from 'components/hooks/useDatetime'
import IconCaret from 'components/parts/Icon/Caret'
import IconHand from 'components/parts/Icon/Hand'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import style from './ContentBase.module.scss'

interface Props {
  media: Media
}

export default function CardMediaContentBase(props: Props): React.JSX.Element {
  const { media } = props
  const { title, read, like, created, channel } = media
  const { name } = channel

  const { formatTimeAgo } = useDatetime()

  return (
    <VStack className={style.content_base}>
      <div title={title} className={style.media_title}>
        {title}
      </div>

      <VStack gap="2" className={style.content}>
        <div className={cx(style.font, style.nickname)}>{name}</div>

        <HStack gap="4">
          <div className={style.font}>
            <IconCaret size="14" className={style.margin} />
            {read}
          </div>
          <div className={style.font}>
            <IconHand size="14" type="off" className={style.margin} />
            {like}
          </div>
        </HStack>

        <time className={style.font}>{formatTimeAgo(created)}</time>
      </VStack>
    </VStack>
  )
}
