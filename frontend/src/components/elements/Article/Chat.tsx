import Link from 'next/link'
import config from 'api/config'
import {ChatResponse} from 'utils/type'
import AuthorSpace from 'components/elements/Common/AuthorSpace'

interface Props {data: ChatResponse}

export default function ArticleChat(props: Props) {
  const {data} = props
  const imageUrl = config.baseUrl + data.author.image
  const nickname = data.author.nickname
  return (
    <section className="section_other" key={data.id}>
      <div className="main_decolation">
        <Link href="/chat/detail/[id]" className="author_space">
          <AuthorSpace imageUrl={imageUrl} nickname={nickname} />
          <div title={ data.title } className="content_title">{ data.title }</div>
          <span className="view_good">
            <div className="view_good_font content_nickname">
              { nickname }
            </div>

            <div className="view_good_font view_good_inline">
              <i title="閲覧数" className="bi bi-caret-right-square"></i>
              { data.read }
            </div>

            <div className="view_good_font view_good_inline">
              <i title="いいね数" className="bi bi-hand-thumbs-up"></i>
              { data.like }
            </div>
            <br/>

            <div className="view_good_font view_good_inline">
              <i title="参加数" className="bi bi-person"></i>
              { data.joined }
            </div>

            <div className="view_good_font view_good_inline">
              <i title="スレッド数" className="bi bi-chat-dots"></i>
              { data.thread }
            </div>
            <br/>

            <div className="view_good_font"><time>{ data.created }</time></div>
          </span>
        </Link>
      </div>
    </section>
  )
}
