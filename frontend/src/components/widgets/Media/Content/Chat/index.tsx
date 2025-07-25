import Link from 'next/link'
import { Chat } from 'types/internal/media'
import AvatarLink from 'components/parts/Avatar/Link'
import HStack from 'components/parts/Stack/Horizontal'
import ChatMediaBaseContent from './Base'
import style from '../MediaContent.module.scss'

interface Props {
  href: string
  media: Chat
}

export default function ChatMediaContent(props: Props): JSX.Element {
  const { href, media } = props
  const { author } = media
  const { avatar, ulid, nickname } = author

  return (
    <div>
      <AvatarLink src={avatar} ulid={ulid} nickname={nickname} className={style.avatar} />
      <Link href={href} className={style.link}>
        <HStack gap="4" className="p_6">
          <div className="mr_36" />
          <ChatMediaBaseContent media={media} />
        </HStack>
      </Link>
    </div>
  )
}
