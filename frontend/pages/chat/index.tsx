import Head from 'next/head'
import ChatArticle from 'components/elements/article/chat'


export default function Chat(props) {
  return (
    <>
      <Head>
        <title>MyUsチャット</title>
      </Head>

      <h1>Chat
        {/* {% if query %} */}
        {/* <section className="messages_search">「{{ query }}」の検索結果「{{ count }}」件</section> */}
        {/* {% endif %} */}
      </h1>

      <ChatArticle/>
    </>
  )
}
