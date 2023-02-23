import Head from 'next/head'
import Link from 'next/link'
import ArticleTodo from 'components/elements/Article/Todo'

export default function Todo() {
  return (
    <>
      <Head>
        <title>MyUsToDo</title>
      </Head>

      <h1>ToDo
        {/* {% if query %} */}
        {/* <section className="search_message">「{{ query }}」の検索結果「{{ count }}」件</section> */}
        {/* {% endif %} */}
      </h1>

      {/* {% if user.is_authenticated %} */}
      <div className="todo_create">
        <Link href="/todo/create" className="btn btn-primary btn-sm">ToDo作成</Link>
      </div>

      <ArticleTodo datas={datas} />

      {/* {% else %} */}
      {/* <h2 className="login_required">ログインしてください</h2> */}
      {/* {% endif %} */}
    </>
  )
}
