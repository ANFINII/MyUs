import Router from 'next/router'
import Main from 'components/layouts/Main'
import Footer from 'components/layouts/Footer'
import Button from 'components/parts/Button'

export default function PasswordChangeDone() {
  return (
    <Main title="パスワード変更">
      <h1>パスワード変更</h1>
      <article className="article_pass">
        <div className="form_account password_done">
          <p className="messages_password_done">パスワードの変更が完了しました!</p>
          <Button blue size="xl" onClick={() => Router.push('/setting/profile')} className="full vertical_24">戻る</Button>
        </div>
        <Footer />
      </article>
    </Main>
  )
}
