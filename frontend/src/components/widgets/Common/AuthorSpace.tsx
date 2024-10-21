import Link from 'next/link'
import ExImage from 'components/parts/ExImage'
import style from './AuthorSpace.module.scss'

interface Props {
  imageUrl: string
  nickname: string
}

export default function AuthorSpace(props: Props) {
  const { imageUrl, nickname } = props

  return (
    <object className={style.author_image_space}>
      <Link href={`/userpage/${nickname}`}>
        <ExImage src={imageUrl} title={nickname} className={style.profile_image} size="32" />
      </Link>
    </object>
  )
}
