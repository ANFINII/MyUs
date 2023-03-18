import Head from 'next/head'
import Router from 'next/router'
import Button from 'components/parts/Button'
import ArticleTodo from 'components/elements/Article_/Todo'
import {MediaResponse} from 'utils/type'


export default function Todo() {
  const datas: Array<MediaResponse> = []
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
        <Button blue size="xs" onClick={() => Router.push('/todo/create')}>ToDo作成</Button>
      </div>

      <ArticleTodo datas={datas} />

      {/* {% else %} */}
      {/* <h2 className="login_required">ログインしてください</h2> */}
      {/* {% endif %} */}
    </>
  )
}
