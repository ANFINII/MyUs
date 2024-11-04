import Link from 'next/link'
import clsx from 'clsx'
import { Author } from 'types/internal/media'
import IconCaret from 'components/parts/Icon/Caret'
import IconHand from 'components/parts/Icon/Hand'
import Horizontal from 'components/parts/Stack/Horizontal'
import AuthorLink from 'components/parts/AuthorLink'
import style from './MediaContent.module.scss'
import Vertical from 'components/parts/Stack/Vertical'
import { formatTimeAgo } from 'utils/functions/datetime'

interface Props {
  href: string
  title: string
  read: number
  totalLike: number
  created: string
  author: Author
}

export default function MediaContent(props: Props) {
  const { href, title, read, totalLike, created, author } = props

  return (
    <Horizontal gap="4" alignment="stretch" className="w_full p_6">
      <AuthorLink imageUrl={author.avatar} nickname={author.nickname} />
      <Link href={href} className="w_full">
        <div title={title} className={style.media_title}>
          {title}
        </div>

        <Vertical gap="2">
          <div className={clsx(style.font, style.nickname)}>{author.nickname}</div>

          <Horizontal gap="4">
            <div className={style.font}>
              <IconCaret size="14" className={style.margin} />
              {read}
            </div>

            <div className={style.font}>
              <IconHand size="14" type="off" className={style.margin} />
              {totalLike}
            </div>
          </Horizontal>

          <time className={style.font}>{formatTimeAgo(created)}</time>
        </Vertical>
      </Link>
    </Horizontal>
  )
}
