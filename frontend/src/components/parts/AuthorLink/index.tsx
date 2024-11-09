import Link from 'next/link'
import Avatar from 'components/parts/Avatar'
import style from './AuthorLink.module.scss'

interface Props {
  imageUrl: string
  nickname: string
}

export default function AuthorLink(props: Props) {
  const { imageUrl, nickname } = props

  return (
    <Link href={`/userpage/${nickname}`} className={style.link}>
      <Avatar size="1.8em" imgSize="32" src={imageUrl} nickname={nickname} className={style.avatar} />
    </Link>
  )
}
