import Link from 'next/link'
import clsx from 'clsx'
import { Chat } from 'types/internal/media'
import { formatTimeAgo } from 'utils/functions/datetime'
import IconCaret from 'components/parts/Icon/Caret'
import IconHand from 'components/parts/Icon/Hand'
import Horizontal from 'components/parts/Stack/Horizontal'
import AuthorLink from 'components/parts/AuthorLink'
import IconPerson from 'components/parts/Icon/Person'
import IconChat from 'components/parts/Icon/Chat'
import Vertical from 'components/parts/Stack/Vertical'
import style from './MediaContent.module.scss'

interface Props {
  href: string
  media: Chat
}

export default function ChatMediaContent(props: Props) {
  const { href, media } = props
  const { title, read, like, joined, thread, created, author } = media
  const { avatar, nickname } = author

  return (
    <Horizontal gap="4" align="stretch" className="p_6">
      <AuthorLink imageUrl={avatar} nickname={nickname} />
      <Link href={href} className={style.link}>
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
      </Link>
    </Horizontal>
  )
}