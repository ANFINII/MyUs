import Link from 'next/link'
import AuthorSpace from 'components/elements/common/author_space'
import ContentTitle from 'components/elements/common/content_title'

export default function PictureArticle() {
  return (
    <article className="article_list">
      {/* {% for item in picture_list %} */}
      <section className="section_list">
        <figure className="main_decolation">
          <Link href="/picture/detail/[id][title]">
            <a><img src="{{ item.image.url }}" width="272" height="153"/></a>
          </Link>
          <Link href="/picture/detail/[id][title]" className="author_space">
            <AuthorSpace/>
            <ContentTitle/>
          </Link>
        </figure>
      </section>
      {/* {% endfor %} */}
    </article>
  )
}
