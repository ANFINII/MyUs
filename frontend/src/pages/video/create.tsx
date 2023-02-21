import Head from 'next/head'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
import InputFile from 'components/parts/Input/File'

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
          <InputFile id="file_1" accept="image/*" required />

          <p className="margin">動画</p>
          <InputFile id="file_2" accept="video/*" required />

          <Button green type="submit" className="button_margin">作成する</Button>
        </form>
      :
        <h2 className="login_required">ログインしてください</h2>
      }
    </>
  )
}
