import Link from 'next/link'

export default function TodoArticle() {
  return (
    <article className="article_list">
      {/* {% for item in todo_list %} */}
      <section className="section_todo">
        {/* {% if item.progress == '2' %} */}
        {/* <div className="main_decolation_todo alert-dark" role="alert"> */}
        {/* {% else %} */}
        <div className="main_decolation_todo alert-{{ item.priority }}" role="alert">
        {/* {% endif %} */}
          <Link href="/todo/detail/[id][title]">
            <a className="author_space_todo">
              {/* <div className="content_title">{{ item.title }}</div>
              <p className="priority">優先度 {{ item.get_priority_display }}</p>
              <p className="progress_myus">進捗度 {{ item.get_progress_display }}</p>
              <time className="todo_time">期日 {{ item.duedate }}</time> */}
              <object className="todo_link">
                <Link href="/todo/update/[id][title]">
                  <a className="btn btn-success btn-sm" role="button">編集</a>
                </Link>
                <Link href="/todo/delete/[id][title]">
                  <a className="btn btn-danger btn-sm" role="button">削除</a>
                </Link>
              </object>
            </a>
          </Link>
        </div>
      </section>
      {/* {% endfor %} */}
    </article>
  )
}
