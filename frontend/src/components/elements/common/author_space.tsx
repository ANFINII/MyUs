import Link from 'next/link'

export default function AuthorSpace(data: any) {
  const author = data.author
  const image_url = process.env.NEXT_PUBLIC_API_URL + author.image
  return (
    <object className="author_image_space">
      <Link href={`/userpage/${author.nickname}`} data-nickname={ author.nickname } className="pjax_button_userpage">
        <img src={ image_url } title={ author.nickname } className="profile_image"/>
      </Link>
    </object>
  )
}
