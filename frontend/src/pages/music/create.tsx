import Head from 'next/head'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'

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
        <Input name="title" id="title" required />

        <p><label htmlFor="content">内容</label></p>
        <Textarea name="content" id="content" required />

        <p><label htmlFor="lyric">歌詞</label></p>
        <Textarea name="lyric" id="lyric" required />

        <p><label htmlFor="custom_file_1">音楽</label></p>
        <div className="form-check">
          <label htmlFor="download" className="form-check-label">ダウンロード許可</label>
          <input type="checkbox" name="download" id="download" className="form-check-input" checked/>
        </div>
        <p><input type="file" name="music" accept="audio/*" id="custom_file_1" className="form-control" style={{display:'none'}} required/></p>
        <p>
          <div className="input-group">
            <input type="text" id="file_1" className="form-control" placeholder="ファイル選択..." onlick="{{$('input[id=custom_file_1]').click()}}"/>
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
