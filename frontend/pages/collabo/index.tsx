import Head from 'next/head'
import AuthorSpace from 'components/elements/author_space'
import ContentTitle from 'components/elements/content_title'

export default function Collabo() {
  return (
    <>
      <Head>
        <title>MyUsコラボ</title>
      </Head>

      <h1>Collabo
        {/* {% if query %} */}
        {/* <section className="messages_search">「{ query }」の検索結果「{{ count }}」件</section> */}
        {/* {% endif %} */}
      </h1>

      <article className="main_article">
        {/* {% for item in collabo_list %} */}
        <section className="main_content_other">
          <div className="main_decolation">
            <a href="{% url 'myus:collabo_detail' item.pk item.title %}" className="author_space">
              <AuthorSpace/>
              <ContentTitle/>
            </a>
          </div>
        </section>
        {/* {% endfor %} */}
      </article>
    </>
  )
}
