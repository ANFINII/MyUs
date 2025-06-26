import Link from 'next/link'
import Avatar from 'components/parts/Avatar'
import style from './AvatarLink.module.scss'

interface Props {
  src: string
  size: string
  nickname: string
  className?: string
}

export default function AvatarLink(props: Props): JSX.Element {
  const { src, size, nickname, className } = props

  return (
    <Link href={`/userpage/${nickname}`} className={className}>
      <Avatar src={src} title={nickname} size={size} color="grey" className={style.avatar} />
    </Link>
  )
}
