import Head from 'next/head'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'

export default function ChatCreate() {
  return (
    <>
      <Head>
        <title>MyUsチャット</title>
      </Head>

      <h1>Chat</h1>
      {/* {% if user.is_authenticated %} */}
      <form method="POST" action="" encType="multipart/form-data">
        {/* {% csrf_token %} */}
        <p><label htmlFor="title">タイトル</label></p>
        <Input name="title" id="title" required />

        <p><label htmlFor="content">内容</label></p>
        <Textarea name="content" id="content" required />

        <p><label htmlFor="id_period">期間</label></p>
        <p><input type="text" name="period" placeholder="2021-12-31" id="id_period" className="form-control" required/></p>
        <br/>

        <p><input type="submit" value="作成する" className="btn btn-success btn-sm"/></p>
      </form>
      {/* {% else %} */}
      <h2 className="login_required">ログインしてください</h2>
      {/* {% endif %} */}
    </>
  )
}
