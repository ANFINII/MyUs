import Head from 'next/head'
import {ChatResponse} from 'utils/type'
import ArticleChat from 'components/elements/Article/Chat'


export default function Chat() {
  const datas: Array<ChatResponse> = []
  return (
    <>
      <Head>
        <title>MyUsチャット</title>
      </Head>

      <h1>Chat
        {/* {% if query %} */}
        {/* <section className="search_message">「{{ query }}」の検索結果「{{ count }}」件</section> */}
        {/* {% endif %} */}
      </h1>

      <ArticleChat datas={datas} />
    </>
  )
}
