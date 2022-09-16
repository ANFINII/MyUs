import Link from 'next/link'
import AuthorSpace from 'components/elements/common/author_space'
import ContentTitle from 'components/elements/common/content_title'

export default function BlogArticle() {
  return (
    <article className="article_list">
      {/* {% for props in blog_list %} */}
      <section className="section_list">
        <figure className="main_decolation">
          <Link href="/blog/detail/[id][title]">
            <a><img src="{{ props.image.url }}" width="272" height="153"/></a>
          </Link>
          <Link href="/blog/detail/[id][title]">
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
