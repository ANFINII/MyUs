import Head from 'next/head'
import CollaboArticle from 'components/elements/article/collabo'

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

      <CollaboArticle/>
    </>
  )
}
