import Link from 'next/link'
import { Chat } from 'types/internal/media'
import AuthorLink from 'components/parts/AuthorLink'
import Horizontal from 'components/parts/Stack/Horizontal'
import ChatMediaBaseContent from './Base'
import style from '../MediaContent.module.scss'

interface Props {
  href: string
  media: Chat
}

export default function ChatMediaContent(props: Props): JSX.Element {
  const { href, media } = props
  const { author } = media
  const { avatar, nickname } = author

  return (
    <div>
      <AuthorLink src={avatar} size="1.8em" imgSize="32" nickname={nickname} className={style.avatar} />
      <Link href={href} className={style.link}>
        <Horizontal gap="4" className="p_6">
          <div className="mr_36" />
          <ChatMediaBaseContent media={media} />
        </Horizontal>
      </Link>
    </div>
  )
}
