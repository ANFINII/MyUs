import Main from 'components/layouts/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'

interface Props {is_authenticated?: boolean}
const now = new Date()
const year = now.getFullYear()

export default function CollaboCreate(props: Props) {
  const {is_authenticated} = props
  return (
    <Main title="MyUsコラボ" hero="Collabo">
      {is_authenticated ?
        <form method="POST" action="" encType="multipart/form-data">
          {/* {% csrf_token %} */}
          <p className="margin">タイトル</p>
          <Input name="title" id="title" required />

          <p className="margin">内容</p>
          <Textarea name="content" id="content" required></Textarea>

          <p className="margin">期間</p>
          <Input name="period" placeholder={`${year}-12-31`} id="id_period" required />

          <Button green type="submit" className="button_margin">作成する</Button>
        </form>
      :
        <h2 className="login_required">ログインしてください</h2>
      }
    </Main>
  )
}
