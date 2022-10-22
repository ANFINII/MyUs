import Link from 'next/link'

export default function AuthorSpace(author: any) {
  return (
    <object className="author_image_space">
      <Link href={`/userpage/${author.nickname}`}>
        <a data-nickname={ author.nickname } className="pjax_button_userpage">
          <img src={ author.image } title={ author.nickname } className="profile_image"/>
        </a>
      </Link>
    </object>
  )
}
