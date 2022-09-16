import Link from 'next/link'
import AuthorSpace from 'components/elements/common/author_space'
import ContentTitle from 'components/elements/common/content_title'

export default function CollaboArticle() {
  return (
    <article className="article_list">
      {/* {% for item in collabo_list %} */}
      <section className="section_other">
        <div className="main_decolation">
          <Link href="/collabo/detail/[id][title]">
            <a href="{% url 'myus:collabo_detail' item.pk item.title %}" className="author_space">
              <AuthorSpace/>
              <ContentTitle/>
            </a>
          </Link>
        </div>
      </section>
      {/* {% endfor %} */}
    </article>
  )
}
