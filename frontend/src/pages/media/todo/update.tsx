import Head from 'next/head'

export default function TodoUpdate() {
  return (
    <>
      <Head>
        <title>MyUsToDo</title>
      </Head>

      <h1>ToDo編集</h1>
      {/* {% if user.isAuth %} */}
      <form method="POST" action="">
        <p>
          <label htmlFor="title">タイトル</label>
        </p>
        <p>
          <input type="text" name="title" value="{{ todo.title }}" id="title" className="form-control" required />
        </p>

        <p>
          <label htmlFor="content">内容</label>
        </p>
        <p>
          <textarea name="content" cols={100} rows={1} id="content" className="form-control textarea" required>
            {/* {todo.content} */}
          </textarea>
        </p>

        <p>
          <label htmlFor="id_priority">優先度</label>
        </p>
        <p>
          <select name="priority" id="id_priority" className="form-control" required>
            {/* {% if object.priority == 'danger' %} */}
            <option value="danger" selected>
              高
            </option>
            <option value="success">普通</option>
            <option value="info">低</option>
            {/* {% elif object.priority == 'success' %}
            <option value="danger">高</option>
            <option value="success" selected>普通</option>
            <option value="info">低</option>
            {% elif object.priority == 'info' %}
            <option value="danger">高</option>
            <option value="success">普通</option>
            <option value="info" selected>低</option>
            {% endif %} */}
          </select>
        </p>

        <p>
          <label htmlFor="id_progress">進捗度</label>
        </p>
        <p>
          <select name="progress" id="id_progress" className="form-control" required>
            {/* {% if object.progress == '0' %} */}
            <option value="0" selected>
              未着手
            </option>
            <option value="1">進行中</option>
            <option value="2">完了</option>
            {/* {% elif object.progress == '1' %}
            <option value="0">未着手</option>
            <option value="1" selected>進行中</option>
            <option value="2">完了</option>
            {% elif object.progress == '2' %}
            <option value="0">未着手</option>
            <option value="1">進行中</option>
            <option value="2" selected>完了</option>
            {% endif %} */}
          </select>
        </p>

        <p>
          <label htmlFor="id_duedate">期日</label>
        </p>
        <p>
          <input type="text" name="duedate" value="{{ todo.duedate|date:'Y-m-j' }}" placeholder="2020-01-01" id="id_duedate" className="form-control" required />
        </p>

        <br />

        <p>
          <input type="submit" value="完了する" className="btn btn-success btn-sm" />
        </p>
      </form>
      {/* {% else %} */}
      {/* <h2 className="login_required">ログインしてください</h2> */}
      {/* {% endif %} */}
    </>
  )
}
