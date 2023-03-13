import Head from 'next/head'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'

export default function CollaboCreate() {
  const is_authenticated = true

  return (
    <>
      <Head>
        <title>MyUsコラボ</title>
      </Head>

      <h1>Collabo</h1>
      {is_authenticated ?
        <form method="POST" action="" encType="multipart/form-data">
          {/* {% csrf_token %} */}
          <p className="margin">タイトル</p>
          <Input name="title" id="title" required />

          <p className="margin">内容</p>
          <Textarea name="content" id="content" required></Textarea>

          <p className="margin">期間</p>
          <Input name="period" placeholder="2021-12-31" id="id_period" required />

          <Button green type="submit" className="button_margin">作成する</Button>
        </form>
      :
        <h2 className="login_required">ログインしてください</h2>
      }
    </>
  )
}
