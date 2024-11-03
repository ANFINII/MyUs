import Link from 'next/link'
import style from './AuthorLink.module.scss'
import Avatar from 'components/parts/Avatar'

interface Props {
  imageUrl: string
  nickname: string
}

export default function AuthorLink(props: Props) {
  const { imageUrl, nickname } = props

  return (
    <Link href={`/userpage/${nickname}`}>
      <Avatar size="1.8em" imgSize="32" src={imageUrl} nickname={nickname} className={style.avatar} />
    </Link>
  )
}
