import Link from 'next/link'
import AuthorSpace from 'components/elements/common/author_space'
import ContentTitle from 'components/elements/common/content_title'

export default function PictureArticle() {
  return (
    <article className="main_article">
      {/* {% for item in picture_list %} */}
      <section className="main_content">
        <figure className="main_decolation">
          <Link href="/picture/detail/[id][title]">
          <a><img src="{{ item.image.url }}" width="272" height="153"/></a>
          </Link>
          <Link href="/picture/detail/[id][title]">
          <a className="author_space">
            <AuthorSpace/>
            <ContentTitle/>
          </a>
          </Link>
        </figure>
      </section>
      {/* {% endfor %} */}
    </article>
  )
}
