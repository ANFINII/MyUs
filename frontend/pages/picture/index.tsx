import Head from 'next/head'
import PictureArticle from 'components/elements/article/picture'


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

      <PictureArticle/>
    </>
  )
}
