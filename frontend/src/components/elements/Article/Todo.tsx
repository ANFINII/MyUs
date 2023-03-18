import Link from 'next/link'
import config from 'api/config'
import {MediaResponse} from 'utils/type'
import AuthorSpace from 'components/elements/Common/AuthorSpace'
import ContentTitle from 'components/elements/Common/ContentTitle'

interface Props {datas: Array<MediaResponse>}

export default function ArticleTodo(props: Props) {
  const {datas} = props
  return (
    <article className="article_list">
      {datas.map((data) => {
        return (
          <section className="section_todo" key={data.id}>
            {/* {% if item.progress == '2' %} */}
            {/* <div className="main_decolation_todo alert-dark" role="alert"> */}
            {/* {% else %} */}
            <div className="main_decolation_todo alert-{{ item.priority }}" role="alert">
            {/* {% endif %} */}
              <Link href="/todo/detail/[id][title]" className="author_space_todo">
                {/* <div className="content_title">{{ item.title }}</div>
                <p className="priority">優先度 {{ item.get_priority_display }}</p>
                <p className="progress_myus">進捗度 {{ item.get_progress_display }}</p>
                <time className="todo_time">期日 {{ item.duedate }}</time> */}
                <object className="todo_link">
                  <Link href="/todo/update/[id][title]" className="btn btn-success btn-sm">編集</Link>
                  <Link href="/todo/delete/[id][title]" className="btn btn-danger btn-sm">削除</Link>
                </object>
              </Link>
            </div>
          </section>
        )
      })}
    </article>
  )
}
