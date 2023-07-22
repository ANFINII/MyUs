import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Select from 'components/parts/Input/Select'
import Textarea from 'components/parts/Input/Textarea'

interface Props {
  isAuthenticated?: boolean
}
const now = new Date()
const year = now.getFullYear()

export const priority = [
  { value: 'danger', label: '高' },
  { value: 'success', label: '普通' },
  { value: 'info', label: '低' },
]

export const progress = [
  { value: '0', label: '未着手' },
  { value: '1', label: '進行中' },
  { value: '2', label: '完了' },
]

export default function TodoCreate(props: Props) {
  const { isAuthenticated } = props
  return (
    <Main title="MyUs Todo" hero="Todo">
      {isAuthenticated ? (
        <form method="POST" action="">
          {/* {% csrf_token %} */}
          <p className="mv_16">タイトル</p>
          <Input name="title" required />

          <p className="mv_16">内容</p>
          <Textarea name="content" required></Textarea>

          <p className="mv_16">優先度</p>
          <Select name="priority" options={priority} />

          <p className="mv_16">進捗度</p>
          <Select name="progress" options={progress} />

          <p className="mv_16">期日</p>
          <Input name="duedate" placeholder={`${year}-12-31`} id="id_duedate" required />

          <Button green type="submit" name="作成する" className="mt_32" />
        </form>
      ) : (
        <h2 className="login_required">ログインしてください</h2>
      )}
    </Main>
  )
}
