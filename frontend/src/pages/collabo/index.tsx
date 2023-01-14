import Head from 'next/head'
import CollaboArticle from 'components/elements/Article/Collabo'

export default function Collabo() {
  return (
    <>
      <Head>
        <title>MyUsコラボ</title>
      </Head>

      <h1>Collabo
        {/* {% if query %} */}
        {/* <section className="search_message">「{ query }」の検索結果「{{ count }}」件</section> */}
        {/* {% endif %} */}
      </h1>

      <CollaboArticle/>
    </>
  )
}
