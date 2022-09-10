import Link from 'next/link'

export default function AuthorSpace() {
  return (
    <object className="author_image_space">
      <Link href="/userpage/[nickname]">
        <a data="{{ item.author.nickname }}" className="pjax_button_userpage">
          <img src="{{ item.author.image }}" title="{{ item.author.nickname }}" className="profile_image"/>
        </a>
      </Link>
    </object>
  )
}
