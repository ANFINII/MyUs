import Head from 'next/head'
import Link from 'next/link'
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
    </>
  )
}
