import Link from 'next/link'
import ExImage from 'components/parts/ExImage'

interface Props {
  imageUrl: string
  nickname: string
}

export default function AuthorSpace(props: Props) {
  const { imageUrl, nickname } = props

  return (
    <object className="author_image_space">
      <Link href={`/userpage/${nickname}`} className="pjax_button_userpage">
        <ExImage src={imageUrl} title={nickname} className="profile_image" size="32" />
      </Link>
    </object>
  )
}
