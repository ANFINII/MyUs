import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import CheckBox from 'components/parts/Input/CheckBox'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'

interface Props {
  isAuth: boolean
}

export default function MusicCreate(props: Props) {
  const { isAuth } = props

  return (
    <Main title="Music">
      <LoginRequired isAuth={isAuth}>
        <form method="POST" action="" encType="multipart/form-data">
          <p className="mv_16">タイトル</p>
          <Input name="title" required />

          <p className="mv_16">内容</p>
          <Textarea name="content" required></Textarea>

          <p className="mv_16">歌詞</p>
          <Textarea name="lyric" required></Textarea>

          <p className="mt_16">音楽</p>
          <CheckBox id="download" labelName="ダウンロード許可" className="mt_2 mb_6" />
          <InputFile accept="audio/*" required />

          <Button color="green" name="作成する" className="mt_32" />
        </form>
      </LoginRequired>
    </Main>
  )
}
