import Main from 'components/layouts/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
import InputFile from 'components/parts/Input/File'

interface Props {is_authenticated?: boolean}

export default function VideoCreate(props: Props) {
  const {is_authenticated} = props
  return (
    <Main title="MyUsビデオ" hero="Video">
      {is_authenticated ?
        <form method="POST" action="" encType="multipart/form-data">
          {/* {% csrf_token %} */}
          <p className="vertical_16">タイトル</p>
          <Input name="title" id="title" required />

          <p className="vertical_16">内容</p>
          <Textarea name="content" id="content" required></Textarea>

          <p className="vertical_16">サムネイル</p>
          <InputFile id="file_1" accept="image/*" required />

          <p className="vertical_16">動画</p>
          <InputFile id="file_2" accept="video/*" required />

          <Button green type="submit" className="top_32">作成する</Button>
        </form>
      :
        <h2 className="login_required">ログインしてください</h2>
      }
    </Main>
  )
}