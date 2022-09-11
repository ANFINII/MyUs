import Head from 'next/head'
import Link from 'next/link'
import TodoArticle from 'components/elements/article/todo'

export default function Todo() {
  return (
    <>
      <Head>
        <title>MyUsToDo</title>
      </Head>

      <h1>ToDo
        {/* {% if query %} */}
        {/* <section className="messages_search">「{{ query }}」の検索結果「{{ count }}」件</section> */}
        {/* {% endif %} */}
      </h1>

      {/* {% if user.is_authenticated %} */}
      <div className="todo_create">
        <Link href="/todo/create">
          <a className="btn btn-primary btn-sm" role="button">ToDo作成</a>
        </Link>
      </div>

      <TodoArticle/>

      {/* {% else %} */}
      {/* <h2 className="login_required">ログインしてください</h2> */}
      {/* {% endif %} */}
    </>
  )
}
