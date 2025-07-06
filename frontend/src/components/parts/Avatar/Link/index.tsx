import Link from 'next/link'
import clsx from 'clsx'
import Avatar from 'components/parts/Avatar'
import style from './AvatarLink.module.scss'

interface Props {
  src: string
  size?: 's' | 'm' | 'l'
  nickname: string
  className?: string
}

export default function AvatarLink(props: Props): JSX.Element {
  const { src, size = 'm', nickname, className } = props

  const sizeValue = size === 's' ? '36' : size === 'm' ? '40' : '48'

  return (
    <Link href={`/userpage/${nickname}`} className={className}>
      {<Avatar src={src} title={nickname} size={sizeValue} color="grey" className={clsx(style.avatar, style[size])} />}
    </Link>
  )
}
