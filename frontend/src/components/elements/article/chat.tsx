import Link from 'next/link'
import AuthorSpace from 'components/elements/Common/AuthorSpace'
import ContentTitle from 'components/elements/Common/ContentTitle'

interface Props {
  imageUrl: string
  nickname: string
}

export default function ChatArticle() {
  return (
    <article className="article_list">
      {/* {% for item in chat_list %} */}
      <section className="section_other">
        <div className="main_decolation">
          <Link href="/chat/detail/[id]" className="author_space">
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
          </Link>
        </div>
      </section>
      {/* {% endfor %} */}
    </article>
  )
}
