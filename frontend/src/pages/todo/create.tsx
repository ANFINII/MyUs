import Head from 'next/head'

export default function TodoCreate() {
  return (
    <>
      <Head>
        <title>MyUsToDo</title>
      </Head>

      <h1>ToDo作成</h1>
      {/* {% if user.is_authenticated %} */}
      <form method="POST" action="">
        {/* {% csrf_token %} */}
        <p><label htmlFor="title">タイトル</label></p>
        <p><input type="text" name="title" id="title" className="form-control" required/></p>

        <p><label htmlFor="content">内容</label></p>
        <p><textarea name="content" cols={100} rows={1} id="content" className="form-control textarea" required></textarea></p>

        <p><label htmlFor="id_priority">優先度</label></p>
        <p>
          <select name="priority" id="id_priority" className="form-control" required>
            <option value="" selected>--------</option>
            <option value="danger">高</option>
            <option value="success">普通</option>
            <option value="info">低</option>
          </select>
        </p>

        <p><label htmlFor="id_progress">進捗度</label></p>
        <p>
          <select name="progress" id="id_progress" className="form-control" required>
            <option value="" selected>--------</option>
            <option value="0">未着手</option>
            <option value="1">進行中</option>
            <option value="2">完了</option>
          </select>
        </p>

        <p><label htmlFor="id_duedate">期日</label></p>
        <p><input type="text" name="duedate" placeholder="2021-12-31" id="id_duedate" className="form-control" required/></p>
        <br/>

        <p><input type="submit" value="作成する" className="btn btn-success btn-sm"/></p>
      </form>
      {/* {% else %} */}
      {/* <h2 className="login_required">ログインしてください</h2> */}
      {/* {% endif %} */}
    </>
  )
}
