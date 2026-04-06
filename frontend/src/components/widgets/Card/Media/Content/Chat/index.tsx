import Link from 'next/link'
import { Chat } from 'types/internal/media'
import AvatarLink from 'components/parts/Avatar/Link'
import HStack from 'components/parts/Stack/Horizontal'
import style from '../Content.module.scss'
import CardChatMediaContentBase from './Base'

interface Props {
  href: string
  media: Chat
}

export default function CardChatMediaContent(props: Props): React.JSX.Element {
  const { href, media } = props
  const { channel } = media
  const { avatar, ownerUlid, name } = channel

  return (
    <div>
      <AvatarLink src={avatar} ulid={ownerUlid} title={name} className={style.avatar} />
      <Link href={href} className={style.link}>
        <HStack gap="4" className="p_6">
          <div className="mr_36" />
          <CardChatMediaContentBase media={media} />
        </HStack>
      </Link>
    </div>
  )
}
