import Link from 'next/link'
import { Todo } from 'types/internal/media'

interface Props {
  data: Todo
}

export default function ArticleTodo(props: Props) {
  const { data } = props
  const { author, id, title } = data
  const { nickname } = author

  return (
    <section className="section_todo">
      {/* {% if data.progress == '2' %} */}
      {/* <div className="main_decolation_todo alert-dark" role="alert"> */}
      {/* {% else %} */}
      <div className="main_decolation_todo alert-{{ data.priority }}" role="alert">
        {/* {% endif %} */}
        <Link href="/todo/detail/[id][title]" className="author_space_todo">
          {/* <div className="content_title">{{ data.title }}</div>
          <p className="priority">優先度 {{ data.get_priority_display }}</p>
          <p className="progress_myus">進捗度 {{ data.get_progress_display }}</p>
          <time className="todo_time">期日 {{ data.duedate }}</time> */}
          <object className="todo_link">
            <Link href={`/media/todo/update/${id}`} className="btn btn-success btn-sm">
              編集
            </Link>
            <Link href={`/media/todo/delete/${id}`} className="btn btn-danger btn-sm">
              削除
            </Link>
          </object>
        </Link>
      </div>
    </section>
  )
}
