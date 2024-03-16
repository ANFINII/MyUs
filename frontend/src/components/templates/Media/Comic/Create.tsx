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

export default function ComicCreate(props: Props) {
  const { isAuth } = props

  return (
    <Main title="Comic">
      <LoginRequired isAuth={isAuth}>
        <form method="POST" action="" encType="multipart/form-data">
          <p className="mv_16">タイトル</p>
          <Input name="title" required />

          <p className="mv_16">内容</p>
          <Textarea name="content" required></Textarea>

          <p className="mv_16">期間</p>
          <Input name="period" placeholder={`${year}-12-31`} required />

          <Button color="green" name="作成する" className="mt_32" />
        </form>
      </LoginRequired>
    </Main>
  )
}
