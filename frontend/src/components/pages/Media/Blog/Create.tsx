import Main from 'components/layouts/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
import InputFile from 'components/parts/Input/File'

interface Props {is_authenticated?: boolean}

export default function BlogCreate(props: Props) {
  const {is_authenticated} = props
  return (
    <Main title="MyUsブログ" hero="Blog">
      {is_authenticated ?
        <form method="POST" action="" encType="multipart/form-data">
          {/* {% csrf_token %} */}
          <p className="margin">タイトル</p>
          <Input name="title" id="title" required />

          <p className="margin">内容</p>
          <Textarea name="content" id="content" required></Textarea>

          <p className="margin">サムネイル</p>
          <InputFile id="file_1" accept="image/*" required />

          <p className="margin">本文</p>
          {/* <p>{{ form.media }}{{ form.richtext }}</p> */}
          <Textarea name="content" id="content" required></Textarea>

          <Button green type="submit" className="button_margin">作成する</Button>
        </form>
      :
        <h2 className="login_required">ログインしてください</h2>
      }
    </Main>
  )
}