import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import InputFile from 'components/parts/Input/File'
import Textarea from 'components/parts/Input/Textarea'

interface Props {
  isAuth?: boolean
}

export default function PictureCreate(props: Props) {
  const { isAuth } = props

  return (
    <Main title="Picture">
      {isAuth ? (
        <form method="POST" action="" encType="multipart/form-data">
          {/* {% csrf_token %} */}
          <p className="mv_16">タイトル</p>
          <Input name="title" required />

          <p className="mv_16">内容</p>
          <Textarea name="content" required></Textarea>

          <p className="mv_16">画像</p>
          <InputFile id="file_1" accept="image/*" required />

          <Button green type="submit" name="作成する" className="mt_32" />
        </form>
      ) : (
        <h2 className="login_required">ログインしてください</h2>
      )}
    </Main>
  )
}
