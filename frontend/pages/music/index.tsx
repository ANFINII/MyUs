import Head from 'next/head'
import MusicArticle from 'components/elements/article/music'

export default function Music() {
  return (
    <>
      <Head>
        <title>MyUsミュージック</title>
      </Head>

      <h1>Music
        {/* {% if query %}
        <section className="search_message">「{{ query }}」の検索結果「{{ count }}」件</section>
        {% endif %} */}
      </h1>

      <MusicArticle/>
    </>
  )
}
