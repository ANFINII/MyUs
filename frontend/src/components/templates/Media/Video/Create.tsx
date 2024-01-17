import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'

interface Props {
  isAuth?: boolean
}

export default function VideoCreate(props: Props) {
  const { isAuth } = props

  return (
    <Main title="Video">
      {isAuth ? (
        <form method="POST" action="" encType="multipart/form-data">
          <p className="mv_16">タイトル</p>
          <Input name="title" id="title" required />

          <p className="mv_16">内容</p>
          <Textarea name="content" id="content" required></Textarea>

          <p className="mv_16">サムネイル</p>
          <InputFile id="file_1" accept="image/*" required />

          <p className="mv_16">動画</p>
          <InputFile id="file_2" accept="video/*" required />

          <Button green type="submit" name="作成する" className="mt_32" />
        </form>
      ) : (
        <h2 className="login_required">ログインしてください</h2>
      )}
    </Main>
  )
}
