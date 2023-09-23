import Layout from 'components/layout'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import CheckBox from 'components/parts/Input/CheckBox'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'

interface Props {
  isAuth?: boolean
}

export default function MusicCreate(props: Props) {
  const { isAuth } = props

  return (
    <Layout title="Music">
      {isAuth ? (
        <form method="POST" action="" encType="multipart/form-data">
          {/* {% csrf_token %} */}
          <p className="mv_16">タイトル</p>
          <Input name="title" id="title" required />

          <p className="mv_16">内容</p>
          <Textarea name="content" id="content" required></Textarea>

          <p className="mv_16">歌詞</p>
          <Textarea name="lyric" id="lyric" required></Textarea>

          <p className="mt_16">音楽</p>
          <CheckBox name="download" id="download" labelName="ダウンロード許可" className="check_margin" />
          <InputFile id="file_1" accept="audio/*" required />

          <Button green type="submit" name="作成する" className="mt_32" />
        </form>
      ) : (
        <h2 className="login_required">ログインしてください</h2>
      )}
    </Layout>
  )
}
