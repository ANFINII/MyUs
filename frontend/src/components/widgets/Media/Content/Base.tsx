import clsx from 'clsx'
import { Media } from 'types/internal/media'
import { formatTimeAgo } from 'utils/functions/datetime'
import IconCaret from 'components/parts/Icon/Caret'
import IconHand from 'components/parts/Icon/Hand'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import style from './MediaContent.module.scss'

interface Props {
  media: Media
}

export default function MediaBaseContent(props: Props) {
  const { media } = props
  const { title, read, like, created, author } = media
  const { nickname } = author

  return (
    <VStack gap="1">
      <div title={title} className={style.media_title}>
        {title}
      </div>

      <VStack gap="2" className={style.content}>
        <div className={clsx(style.font, style.nickname)}>{nickname}</div>

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
