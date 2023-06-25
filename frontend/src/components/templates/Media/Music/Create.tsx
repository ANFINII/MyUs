import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
import CheckBox from 'components/parts/Input/CheckBox'
import InputFile from 'components/parts/Input/File'

interface Props {is_authenticated?: boolean}

export default function MusicCreate(props: Props) {
  const {is_authenticated} = props
  return (
    <Main title="MyUsミュージック" hero="Music">
      {is_authenticated ?
        <form method="POST" action="" encType="multipart/form-data">
          {/* {% csrf_token %} */}
          <p className="mv_16">タイトル</p>
          <Input name="title" id="title" required />

          <p className="mv_16">内容</p>
          <Textarea name="content" id="content" required></Textarea>

          <p className="mv_16">歌詞</p>
          <Textarea name="lyric" id="lyric" required></Textarea>

          <p className="mt_16">音楽</p>
          <CheckBox name="download" id="download" className="check_margin" checked>ダウンロード許可</CheckBox>
          <InputFile id="file_1" accept="audio/*" required />

          <Button green type="submit" className="mt_32">作成する</Button>
        </form>
      :
        <h2 className="login_required">ログインしてください</h2>
      }
    </Main>
  )
}
