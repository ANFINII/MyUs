import Head from 'next/head'
import Link from 'next/link'
import AuthorSpace from 'components/elements/author_space'
import ContentTitle from 'components/elements/content_title'

export default function Blog(props) {
  return (
    <>
      <Head>
        <title>MyUsブログ</title>
      </Head>

      <h1>Blog
        {/* if (props.query) { */}
        <section className="messages_search">「{ props.query }」の検索結果「{ props.count }」件</section>
        {/* } */}
      </h1>

      <article className="main_article">
        {/* {% for props in blog_list %} */}
        <section className="main_content">
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
    </>
  )
}
