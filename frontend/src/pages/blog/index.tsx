import Head from 'next/head'
import BlogArticle from 'components/elements/article/blog'

export default function Blog() {
  return (
    <>
      <Head>
        <title>MyUsブログ</title>
      </Head>

      <h1>Blog
        {/* if (props.query) { */}
        {/* <section className="search_message">「{ props.query }」の検索結果「{ props.count }」件</section> */}
        {/* } */}
      </h1>

      <BlogArticle/>
    </>
  )
}
