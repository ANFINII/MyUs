import Head from 'next/head'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'

export default function VideoCreate() {
  const is_authenticated = true

  return (
    <>
      <Head>
        <title>MyUsビデオ</title>
      </Head>

      <h1>Video</h1>
      {is_authenticated ?
        <form method="POST" action="" encType="multipart/form-data">
          {/* {% csrf_token %} */}
          <p className="margin">タイトル</p>
          <Input name="title" id="title" required />

          <p className="margin">内容</p>
          <Textarea name="content" id="content" required />

          <p className="margin">サムネイル</p>
          <input type="file" name="image" accept="image/*" id="custom_file_1" className="form-control" style={{display:'none'}} required/>
          <input type="text" id="file_1" className="form-control" placeholder="ファイル選択..." onClick="$('input[id=custom_file_1]').click()"/>

          <p className="margin">動画</p>
          <input type="file" name="convert" accept="video/*" id="custom_file_2" className="form-control" style={{display:'none'}} required/>
          <input type="text" id="file_2" className="form-control" placeholder="ファイル選択..." onClick="$('input[id=custom_file_2]').click()"/>

          <Button green type="submit" className="button_margin">作成する</Button>
        </form>
      :
        <h2 className="login_required">ログインしてください</h2>
      }

      {/* {% block extrajs %} */}
      <script src="{% static 'js/attachment_name.js' %}"></script>
      {/* {% endblock extrajs %} */}
    </>
  )
}
