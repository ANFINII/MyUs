import Head from 'next/head'
import {ImageResponse} from 'utils/type'
import PictureArticle from 'components/elements/Article_/Picture'


export default function Picture() {
  const datas: Array<ImageResponse> = []
  return (
    <>
      <Head>
        <title>MyUsピクチャー</title>
      </Head>

      <h1>Picture
        {/* {% if query %} */}
        {/* <section className="search_message">「{{ query }}」の検索結果「{{ count }}」件</section> */}
        {/* {% endif %} */}
      </h1>

      <PictureArticle datas={datas} />
    </>
  )
}
