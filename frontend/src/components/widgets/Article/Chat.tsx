import Link from 'next/link'
import { Chat } from 'types/internal/media'
import AuthorSpace from 'components/widgets/Common/AuthorSpace'

interface Props {
  data: Chat
}

export default function ArticleChat(props: Props) {
  const { data } = props
  const { author, id, title, read, like, joined, thread, created } = data
  const { nickname, image } = author

  return (
    <section className="section_other">
      <div className="main_decolation">
        <Link href={`/media/chat/${id}`} className="author_space">
          <AuthorSpace imageUrl={image} nickname={nickname} />
          <div title={title} className="content_title">
            {title}
          </div>
          <span className="view_good">
            <div className="view_good_font content_nickname">{nickname}</div>

            <div className="view_good_font view_good_inline">
              <i title="閲覧数" className="bi bi-caret-right-square"></i>
              {read}
            </div>

            <div className="view_good_font view_good_inline">
              <i title="いいね数" className="bi bi-hand-thumbs-up"></i>
              {like}
            </div>
            <br />

            <div className="view_good_font view_good_inline">
              <i title="参加数" className="bi bi-person"></i>
              {joined}
            </div>

            <div className="view_good_font view_good_inline">
              <i title="スレッド数" className="bi bi-chat-dots"></i>
              {thread}
            </div>
            <br />

            <div className="view_good_font">
              <time>{created}</time>
            </div>
          </span>
        </Link>
      </div>
    </section>
  )
}
