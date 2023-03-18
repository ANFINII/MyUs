import Head from 'next/head'
import {ImageResponse} from 'utils/type'
import ArticleBlog from 'components/elements/Article_/Blog'

export default function Blog() {
  const datas: Array<ImageResponse> = []
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

      <ArticleBlog datas={datas} />
    </>
  )
}
