export default function CollaboCreate() {
  return (
    <>
      <h1>Collabo</h1>
      {/* {% if user.is_authenticated %} */}
      <form method="POST" action="" enctype="multipart/form-data">
        {/* {% csrf_token %} */}
        <p><label htmlFor="title">タイトル</label></p>
        <p><input type="text" name="title" id="title" className="form-control" required/></p>

        <p><label htmlFor="content">内容</label></p>
        <p><textarea name="content" cols={100} rows={1} id="content" className="form-control textarea" required></textarea></p>

        <p><label htmlFor="id_period">期間</label></p>
        <p><input type="text" name="period" id="id_period" className="form-control" placeholder="2021-12-31" required/></p>
        <br/>

        <p><input type="submit" value="作成する" className="btn btn-success btn-sm"/></p>
      </form>
      {/* {% else %}
      <h2 className="login_required">ログインしてください</h2>
      {% endif %} */}
    </>
  )
}
