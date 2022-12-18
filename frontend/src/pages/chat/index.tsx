import Head from 'next/head'
import ChatArticle from 'components/elements/article/chat'


export default function Chat() {
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

      <ChatArticle/>
    </>
  )
}
