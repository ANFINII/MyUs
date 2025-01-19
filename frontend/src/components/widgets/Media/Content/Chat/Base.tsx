import clsx from 'clsx'
import { Chat } from 'types/internal/media'
import { formatTimeAgo } from 'utils/functions/datetime'
import IconCaret from 'components/parts/Icon/Caret'
import IconChat from 'components/parts/Icon/Chat'
import IconHand from 'components/parts/Icon/Hand'
import IconPerson from 'components/parts/Icon/Person'
import Horizontal from 'components/parts/Stack/Horizontal'
import Vertical from 'components/parts/Stack/Vertical'
import style from '../MediaContent.module.scss'

interface Props {
  media: Chat
}

export default function ChatMediaBaseContent(props: Props): JSX.Element {
  const { media } = props
  const { title, read, like, joined, thread, created, author } = media
  const { nickname } = author

  return (
    <Vertical gap="1">
      <div title={title} className={style.media_title}>
        {title}
      </div>

      <Vertical gap="2">
        <div className={clsx(style.font, style.nickname)}>{nickname}</div>

        <Horizontal gap="4">
          <div className={style.font}>
            <IconCaret size="14" className={style.margin} />
            {read}
          </div>
          <div className={style.font}>
            <IconHand size="14" type="off" className={style.margin} />
            {like}
          </div>
        </Horizontal>

        <Horizontal gap="4">
          <div className={style.font}>
            <IconPerson size="14" type="base" className={style.margin} />
            {joined}
          </div>
          <div className={style.font}>
            <IconChat size="14" className={style.margin} />
            {thread}
          </div>
        </Horizontal>

        <time className={style.font}>{formatTimeAgo(created)}</time>
      </Vertical>
    </Vertical>
  )
}
