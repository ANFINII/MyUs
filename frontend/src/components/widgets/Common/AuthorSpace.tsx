import Link from 'next/link'
import Image from 'next/image'

interface Props {
  imageUrl: string
  nickname: string
}

export default function AuthorSpace(props: Props) {
  const { imageUrl, nickname } = props

  return (
    <object className="author_image_space">
      <Link href={`/userpage/${nickname}`} className="pjax_button_userpage">
        <Image src={imageUrl} title={nickname} className="profile_image" width={32} height={32} alt="" />
      </Link>
    </object>
  )
}
