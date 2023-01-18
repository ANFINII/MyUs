import Head from 'next/head'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'

export default function BlogCreate() {
  return (
    <>
      <Head>
        <title>MyUsブログ</title>
      </Head>

      <h1>Blog</h1>
      {/* {% if user.is_authenticated %} */}
      <form method="POST" action="" encType="multipart/form-data">
        {/* {% csrf_token %} */}
        <p><label htmlFor="title">タイトル</label></p>
        <Input name="title" id="title" required />

        <p><label htmlFor="content">内容</label></p>
        <Textarea name="content" id="content" required />

        <p><label htmlFor="custom_file_1">サムネイル</label></p>
        <p>
          <input type="file" name="image" accept="image/*" id="custom_file_1" className="form-control" style={{display:'none'}} required/>
          <div className="input-group">
            {/* <input type="text" id="file_1" className="form-control" placeholder="ファイル選択..." onclick={$('input[id=custom_file_1]').click()}/> */}
          </div>
        </p>

        <p>本文</p>
        {/* <p>{{ form.media }}{{ form.richtext }}</p> */}
        <Textarea name="content" id="content" required />
        <br/>

        <p><input type="submit" value="作成する" className="btn btn-success btn-sm"/></p>
      </form>
      {/* {% else %}
      <h2 className="login_required">ログインしてください</h2>
      {% endif %} */}
    </>
  )
}
