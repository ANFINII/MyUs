import Link from 'next/link'
import { Media } from 'types/internal/media/output'
import AvatarLink from 'components/parts/Avatar/Link'
import HStack from 'components/parts/Stack/Horizontal'
import CardMediaContentBase from './Base'
import style from './Content.module.scss'

interface Props<Media> {
  href: string
  media: Media
}

export default function CardMediaContent(props: Props<Media>) {
  const { href, media } = props
  const { channel } = media
  const { avatar, ownerUlid, name } = channel

  return (
    <div>
      <AvatarLink src={avatar} ulid={ownerUlid} title={name} className={style.avatar} />
      <Link href={href} className={style.link}>
        <HStack gap="4" className="p_6">
          <div className="mr_36" />
          <CardMediaContentBase media={media} />
        </HStack>
      </Link>
    </div>
  )
}
