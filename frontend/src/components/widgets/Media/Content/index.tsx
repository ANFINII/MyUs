import Link from 'next/link'
import { Media } from 'types/internal/media'
import AvatarLink from 'components/parts/Avatar/Link'
import HStack from 'components/parts/Stack/Horizontal'
import MediaBaseContent from './Base'
import style from './MediaContent.module.scss'

interface Props<Media> {
  href: string
  media: Media
}

export default function MediaContent(props: Props<Media>) {
  const { href, media } = props
  const { author } = media
  const { avatar, nickname } = author

  return (
    <div>
      <AvatarLink src={avatar} size="40" nickname={nickname} className={style.avatar} />
      <Link href={href} className={style.link}>
        <HStack gap="4" className="p_6">
          <div className="mr_36" />
          <MediaBaseContent media={media} />
        </HStack>
      </Link>
    </div>
  )
}
