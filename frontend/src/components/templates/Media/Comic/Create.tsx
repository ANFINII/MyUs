import Layout from 'components/layout'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'

interface Props {
  isAuth?: boolean
}
const now = new Date()
const year = now.getFullYear()

export default function ComicCreate(props: Props) {
  const { isAuth } = props

  return (
    <Layout title="Comic">
      {isAuth ? (
        <form method="POST" action="" encType="multipart/form-data">
          {/* {% csrf_token %} */}
          <p className="mv_16">タイトル</p>
          <Input name="title" id="title" required />

          <p className="mv_16">内容</p>
          <Textarea name="content" id="content" required></Textarea>

          <p className="mv_16">期間</p>
          <Input name="period" placeholder={`${year}-12-31`} id="id_period" required />

          <Button green type="submit" name="作成する" className="mt_32" />
        </form>
      ) : (
        <h2 className="login_required">ログインしてください</h2>
      )}
    </Layout>
  )
}
