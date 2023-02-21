import Head from 'next/head'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
import InputFile from 'components/parts/Input/File'

export default function PictureCreate() {
  const is_authenticated = true

  return (
    <>
      <Head>
        <title>MyUsピクチャー</title>
      </Head>

      <h1>Picture</h1>
      {is_authenticated ?
        <form method="POST" action="" encType="multipart/form-data">
          {/* {% csrf_token %} */}
          <p className="margin">タイトル</p>
          <Input name="title" required />

          <p className="margin">内容</p>
          <Textarea name="content" required />

          <p className="margin">画像</p>
          <InputFile id="file_1" accept="image/*" required />

          <Button green type="submit" className="button_margin">作成する</Button>
        </form>
      :
        <h2 className="login_required">ログインしてください</h2>
      }
    </>
  )
}
