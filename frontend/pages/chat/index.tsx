import Head from 'next/head'
import Link from 'next/link'
import AuthorSpace from 'components/elements/author_space'
import ContentTitle from 'components/elements/content_title'

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

      <article className="main_article">
        {/* {% for item in chat_list %} */}
        <section className="main_content_other">
          <div className="main_decolation">
            <Link href="/chat/detail/[id]">
              <a className="author_space">
                <AuthorSpace/>
                <ContentTitle/>
                {/* <div title="{{ item.title }}" className="content_title">{{ item.title }}</div> */}
                <span className="view_good">
                  <div className="view_good_font content_nickname">
                    {/* {{ item.author.nickname }} */}
                  </div>

                  <div className="view_good_font view_good_inline">
                    <i title="閲覧数" className="bi bi-caret-right-square"></i>
                    {/* {{ item.read|intcomma }} */}
                  </div>

                  <div className="view_good_font view_good_inline">
                    <i title="いいね数" className="bi bi-hand-thumbs-up"></i>
                    {/* {{ item.total_like|intcomma }} */}
                  </div>
                  <br/>

                  <div className="view_good_font view_good_inline">
                    <i title="参加数" className="bi bi-person"></i>
                    {/* {{ item.joined|intcomma }} */}
                  </div>

                  <div className="view_good_font view_good_inline">
                    <i title="スレッド数" className="bi bi-chat-dots"></i>
                    {/* {{ item.thread|intcomma }} */}
                  </div>
                  <br/>

                  {/* <div className="view_good_font"><time>{{ item.created|naturaltime }}</time></div> */}
                </span>
              </a>
            </Link>
          </div>
        </section>
        {/* {% endfor %} */}
      </article>
    </>
  )
}
