import Link from 'next/link'
import clsx from 'clsx'
import { Media } from 'types/internal/media'
import { formatTimeAgo } from 'utils/functions/datetime'
import AuthorLink from 'components/parts/AuthorLink'
import IconCaret from 'components/parts/Icon/Caret'
import IconHand from 'components/parts/Icon/Hand'
import Horizontal from 'components/parts/Stack/Horizontal'
import Vertical from 'components/parts/Stack/Vertical'
import style from './MediaContent.module.scss'

interface Props<Media> {
  href: string
  media: Media
}

export default function MediaContent(props: Props<Media>) {
  const { href, media } = props
  const { title, read, like, created, author } = media
  const { avatar, nickname } = author

  return (
    <div>
      <AuthorLink imageUrl={avatar} nickname={nickname} className={style.avatar} />
      <Link href={href} className={style.link}>
        <Horizontal gap="4" className="p_6">
          <div className='mr_36' />
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

              <time className={style.font}>{formatTimeAgo(created)}</time>
            </Vertical>
          </Vertical>
        </Horizontal>
      </Link>
    </div>
  )
}
