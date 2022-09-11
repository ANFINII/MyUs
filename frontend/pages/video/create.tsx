import Head from 'next/head'

export default function VideoCreate() {
  return (
    <>
      <Head>
        <title>MyUsビデオ</title>
      </Head>

      <h1>Video</h1>
      {/* {% if user.is_authenticated %} */}
      <form method="POST" action="" encType="multipart/form-data">
        {/* {% csrf_token %} */}
        <p><label htmlFor="title">タイトル</label></p>
        <p><input type="text" name="title" id="title" className="form-control" required/></p>

        <p><label htmlFor="content">内容</label></p>
        <p><textarea name="content" cols={100} rows={1} id="content" className="form-control textarea" required></textarea></p>

        <p><label htmlFor="custom_file_1">サムネイル</label></p>
        <p>
          <input type="file" name="image" accept="image/*" id="custom_file_1" className="form-control" style={{display:'none'}} required/>
          <div className="input-group">
            <input type="text" id="file_1" className="form-control" placeholder="ファイル選択..." onclick="$('input[id=custom_file_1]').click();"/>
          </div>
        </p>

        <p><label htmlFor="custom_file_2">動画</label></p>
        <p>
          <input type="file" name="convert" accept="video/*" id="custom_file_2" className="form-control" style={{display:'none'}} required/>
          <div className="input-group">
            <input type="text" id="file_2" className="form-control" placeholder="ファイル選択..." onclick="$('input[id=custom_file_2]').click();"/>
          </div>
        </p>
        <br/>

        <p><input type="submit" value="作成する" className="btn btn-success btn-sm"/></p>
      </form>
      {/* {% else %} */}
      {/* <h2 className="login_required">ログインしてください</h2> */}
      {/* {% endif %} */}

      {/* {% block extrajs %} */}
      <script src="{% static 'js/attachment_name.js' %}"></script>
      {/* {% endblock extrajs %} */}
    </>
  )
}