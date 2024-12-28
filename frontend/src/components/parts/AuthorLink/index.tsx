import Link from 'next/link'
import clsx from 'clsx'
import Avatar from 'components/parts/Avatar'
import style from './AuthorLink.module.scss'

interface Props {
  src: string
  size: string
  imgSize: string
  nickname: string
  className?: string
}

export default function AuthorLink(props: Props) {
  const { src, size, imgSize, nickname, className } = props

  return (
    <Link href={`/userpage/${nickname}`} className={clsx(style.link, className)}>
      <Avatar src={src} title={nickname} size={size} imgSize={imgSize} color="grey" className={style.avatar} />
    </Link>
  )
}
