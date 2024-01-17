import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'

const now = new Date()
const year = now.getFullYear()

interface Props {
  isAuth: boolean
}

export default function ChatCreate(props: Props) {
  const { isAuth } = props

  return (
    <Main title="Chat">
      <LoginRequired isAuth={isAuth}>
        <form method="POST" action="" encType="multipart/form-data">
          <p className="mv_16">タイトル</p>
          <Input name="title" id="title" required />

          <p className="mv_16">内容</p>
          <Textarea name="content" id="content" required></Textarea>

          <p className="mv_16">期間</p>
          <Input name="period" placeholder={`${year}-12-31`} id="id_period" required />

          <Button green type="submit" name="作成する" className="mt_32" />
        </form>
      </LoginRequired>
    </Main>
  )
}
