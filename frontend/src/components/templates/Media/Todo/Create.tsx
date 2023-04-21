import Main from 'components/layouts/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'

interface Props {is_authenticated?: boolean}
const now = new Date()
const year = now.getFullYear()

export default function TodoCreate(props: Props) {
  const {is_authenticated} = props
  return (
    <Main title="MyUs Todo" hero="Todo">
      {is_authenticated ?
        <form method="POST" action="">
          {/* {% csrf_token %} */}
          <p className="margin">タイトル</p>
          <Input name="title" required />

          <p className="margin">内容</p>
          <Textarea name="content" required></Textarea>

          <p className="margin">優先度</p>
          <select name="priority" id="id_priority" className="form-control" required>
            <option value="" selected>--------</option>
            <option value="danger">高</option>
            <option value="success">普通</option>
            <option value="info">低</option>
          </select>

          <p className="margin">進捗度</p>
          <select name="progress" id="id_progress" className="form-control" required>
            <option value="" selected>--------</option>
            <option value="0">未着手</option>
            <option value="1">進行中</option>
            <option value="2">完了</option>
          </select>

          <p>期日</p>
          <Input name="duedate" placeholder={`${year}-12-31`} id="id_duedate" required />
          <br/>

          <Button green type="submit" className="button_margin">作成する</Button>
        </form>
      :
        <h2 className="login_required">ログインしてください</h2>
      }
    </Main>
  )
}
