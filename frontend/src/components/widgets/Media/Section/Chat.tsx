import Link from 'next/link'
import clsx from 'clsx'
import { Chat } from 'types/internal/media'
import AuthorLink from 'components/parts/AuthorLink'
import style from './Section.module.scss'

interface Props {
  data: Chat
}

export default function SectionChat(props: Props) {
  const { data } = props
  const { author, id, title, read, like, joined, thread, created } = data
  const { nickname, avatar } = author

  return (
    <section className={style.section_other}>
      <div className={style.decolation}>
        <Link href={`/media/chat/${id}`} className={style.author_space}>
          <AuthorLink imageUrl={avatar} nickname={nickname} />
          <div title={title} className="content_title">
            {title}
          </div>
          <span className={style.view_good}>
            <div className={clsx(style.view_good_font, style.content_nickname)}>{nickname}</div>

            <div className={clsx(style.view_good_font, style.view_good_inline)}>
              <i title="閲覧数" className="bi bi-caret-right-square"></i>
              {read}
            </div>

            <div className={clsx(style.view_good_font, style.view_good_inline)}>
              <i title="いいね数" className="bi bi-hand-thumbs-up"></i>
              {like}
            </div>
            <br />

            <div className={clsx(style.view_good_font, style.view_good_inline)}>
              <i title="参加数" className="bi bi-person"></i>
              {joined}
            </div>

            <div className={clsx(style.view_good_font, style.view_good_inline)}>
              <i title="スレッド数" className="bi bi-chat-dots"></i>
              {thread}
            </div>
            <br />

            <div className={style.view_good_font}>
              <time>{created}</time>
            </div>
          </span>
        </Link>
      </div>
    </section>
  )
}
