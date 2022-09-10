import Head from 'next/head'

export default function MusicCreate() {
  return (
    <>
      <Head>
        <title>MyUsミュージック</title>
      </Head>

      <h1>Music</h1>
      {/* {% if user.is_authenticated %} */}
      <form method="POST" action="" encType="multipart/form-data">
        {/* {% csrf_token %} */}
        <p><label htmlFor="title">タイトル</label></p>
        <p><input type="text" name="title" id="title" className="form-control" required/></p>

        <p><label htmlFor="content">内容</label></p>
        <p><textarea name="content" cols={100} rows={1} id="content" className="form-control textarea" required></textarea></p>

        <p><label htmlFor="lyric">歌詞</label></p>
        <p><textarea name="lyric" cols={100} rows={1} id="lyric" className="form-control textarea"></textarea></p>

        <p><label htmlFor="custom_file_1">音楽</label></p>
        <div className="form-check">
          <label htmlFor="download" className="form-check-label">ダウンロード許可</label>
          <input type="checkbox" name="download" id="download" className="form-check-input" checked/>
        </div>
        <p><input type="file" name="music" accept="audio/*" id="custom_file_1" className="form-control" style={{display:'none'}} required/></p>
        <p>
          <div className="input-group">
            <input type="text" id="file_1" className="form-control" placeholder="ファイル選択..." onclick="{{$('input[id=custom_file_1]').click();}}"/>
          </div>
        </p>
        <br/>

        <p><input type="submit" value="作成する" className="btn btn-success btn-sm"/></p>
      </form>
      {/* {% else %} */}
      {/* <h2 className="login_required">ログインしてください</h2> */}
      {/* {% endif %} */}

      {/* {% block extrajs %} */}
      <script src="/js/attachment_name.js"></script>
      {/* {% endblock extrajs %} */}
    </>
  )
}
