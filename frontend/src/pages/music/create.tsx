import Head from 'next/head'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
import CheckBox from 'components/parts/Input/CheckBox'
import InputFile from 'components/parts/Input/File'

export default function MusicCreate() {
  const is_authenticated = true

  return (
    <>
      <Head>
        <title>MyUsミュージック</title>
      </Head>

      <h1>Music</h1>
      {is_authenticated ?
        <form method="POST" action="" encType="multipart/form-data">
          {/* {% csrf_token %} */}
          <p className="margin">タイトル</p>
          <Input name="title" id="title" required />

          <p className="margin">内容</p>
          <Textarea name="content" id="content" required />

          <p className="margin">歌詞</p>
          <Textarea name="lyric" id="lyric" required />

          <p className="margin_top">音楽</p>
          <CheckBox name="download" id="download" checked>ダウンロード許可</CheckBox>
          <InputFile id="file_1" accept="audio/*" />

          <Button green type="submit" className="button_margin">作成する</Button>
        </form>
      :
        <h2 className="login_required">ログインしてください</h2>
      }
    </>
  )
}
