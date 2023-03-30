import Head from 'next/head'

export default function TodoDelete() {
  return (
    <>
      <Head>
        <title>MyUsToDo</title>
      </Head>

      <h1>ToDo削除</h1>
      {/* {% if user.is_authenticated %} */}
      {/* <p>タイトル：{{ object.title }}</p>

      <p>優先度：{{ object.get_priority_display }}</p>

      <p>進捗度：{{ object.get_progress_display }}</p>

      <p>期日：{{ todo.duedate|date:'Y-m-j' }}</p>

      <p>内容：{{ todo.content }}</p> */}

      <br />

      <form method="POST" action="">
        {/* {% csrf_token %} */}
        <input type="submit" value="削除する" className="btn btn-danger btn-sm" />
      </form>
      {/* {% else %} */}
      <h2 className="login_required">ログインしてください</h2>
      {/* {% endif %} */}
    </>
  )
}
