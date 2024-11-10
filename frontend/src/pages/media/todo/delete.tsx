import Main from 'components/layout/Main'
import LoginError from 'components/parts/Error/Login'

export default function TodoDelete() {
  return (
    <Main title="Todo">
      <LoginError>
        <h1>ToDo削除</h1>
        {/* {% if user.isAuth %} */}
        {/* <p>タイトル：{{ object.title }}</p>

      <p>優先度：{{ object.get_priority_display }}</p>

      <p>進捗度：{{ object.get_progress_display }}</p>

      <p>期日：{{ todo.duedate|date:'Y-m-j' }}</p>

      <p>内容：{{ todo.content }}</p> */}

        <br />

        <form method="POST" action="">
          <input type="submit" value="削除する" className="btn btn-danger btn-sm" />
        </form>
      </LoginError>
    </Main>
  )
}
