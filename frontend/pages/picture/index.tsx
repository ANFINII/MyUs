import Head from 'next/head'
import AuthorSpace from 'components/elements/author_space'
import ContentTitle from 'components/elements/content_title'

export default function Picture() {
  return (
    <>
      <Head>
        <title>MyUsピクチャー</title>
      </Head>

      <h1>Picture
        {/* {% if query %} */}
        {/* <section className="messages_search">「{{ query }}」の検索結果「{{ count }}」件</section> */}
        {/* {% endif %} */}
      </h1>

      <article className="main_article">
        {/* {% for item in picture_list %} */}
        <section className="main_content">
          <figure className="main_decolation">
            <a href="{% url 'myus:picture_detail' item.pk item.title %}">
              <img src="{{ item.image.url }}" width="272" height="153"/>
            </a>
            <a href="{% url 'myus:picture_detail' item.pk item.title %}" className="author_space">
              <AuthorSpace/>
              <ContentTitle/>
            </a>
          </figure>
        </section>
        {/* {% endfor %} */}
      </article>
    </>
  )
}
