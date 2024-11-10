import Link from 'next/link'
import clsx from 'clsx'
import Avatar from 'components/parts/Avatar'
import style from './AuthorLink.module.scss'

interface Props {
  imageUrl: string
  nickname: string
  className?: string
}

export default function AuthorLink(props: Props) {
  const { imageUrl, nickname, className } = props

  return (
    <Link href={`/userpage/${nickname}`} className={clsx(style.link, className)}>
      <Avatar size="1.8em" imgSize="32" src={imageUrl} nickname={nickname} className={style.avatar} />
    </Link>
  )
}
