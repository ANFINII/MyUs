import Head from 'next/head'
import Link from 'next/link'
import AuthorSpace from 'components/elements/author_space'
import ContentTitle from 'components/elements/content_title'

export default function Music() {
  return (
    <>
      <Head>
        <title>MyUsミュージック</title>
      </Head>

      <h1>Music
        {/* {% if query %}
        <section className="messages_search">「{{ query }}」の検索結果「{{ count }}」件</section>
        {% endif %} */}
      </h1>

      <article className="main_article">
        {/* {% for item in music_list %} */}
        <section className="main_content_music">
          <div className="main_decolation">
            <audio controls controlslist="nodownload" preload="none" className="audio_auto">
              <source src="{{ item.music.url }}"/>
              <p>ブラウザがaudioに対応しておりません</p>
            </audio>
            <Link href="/music/detail/[id][title]">
            <a className="author_space">
              <AuthorSpace/>
              <ContentTitle/>
            </a>
            </Link>
          </div>
        </section>
        {/* {% endfor %} */}
      </article>
    </>
  )
}
